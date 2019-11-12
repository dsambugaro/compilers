#! /usr/bin/env python3
# coding: utf-8

import logging
from sys import argv, exit

from ctypes import CFUNCTYPE, c_int
from llvmlite import ir, binding
from termcolor import colored
from anytree import PreOrderIter

import parser
import semantic
from utils import get_leaves, get_leaves_index
from MyExceptions import SemanticError


class CodeGen():
    def __init__(self, root, symbol_table, filename):
        self.root = root
        self.symbol_table = symbol_table
        self.functions = []
        self.variables = []
        self.globalVariables = []
        self.filename = filename

        self.int = ir.IntType(32)
        self.intInitializer = ir.Constant(ir.IntType(32), 0)
        self.floatInitializer = ir.Constant(ir.FloatType(), 0.0)
        self.float = ir.FloatType()

        self.binding = binding
        self.binding.initialize()
        self.binding.initialize_native_target()
        self.binding.initialize_native_asmprinter()
        self._config_llvm()
        self._create_execution_engine()
        self._declare_io_functions()

    def _config_llvm(self):
        self.module = ir.Module(name=self.filename)
        self.module.triple = self.binding.get_default_triple()

    def _create_execution_engine(self):
        target = self.binding.Target.from_default_triple()
        target_machine = target.create_target_machine()
        backing_mod = binding.parse_assembly("")
        engine = binding.create_mcjit_compiler(backing_mod, target_machine)
        self.engine = engine

    def _declare_io_functions(self):
        self.voidptr_ty = ir.IntType(8).as_pointer()
        scanf_ty = ir.FunctionType(ir.IntType(
            32), [self.voidptr_ty], var_arg=True)
        scanf = ir.Function(self.module, scanf_ty, name="__isoc99_scanf")
        self.scanf = scanf

        self.voidptr_ty = ir.IntType(8).as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(
            32), [self.voidptr_ty], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name="printf")
        self.printf = printf

        int_fmt_scan = "%i\0"
        int_c_fmt_scan = ir.Constant(ir.ArrayType(ir.IntType(8), len(int_fmt_scan)),
                                     bytearray(int_fmt_scan.encode("utf8")))
        self.int_global_fmt_scan = ir.GlobalVariable(
            self.module, int_c_fmt_scan.type, name="fstr_int_scan")
        self.int_global_fmt_scan.linkage = 'internal'
        self.int_global_fmt_scan.align = 4
        self.int_global_fmt_scan.initializer = int_c_fmt_scan

        float_fmt_scan = "%f\0"
        flo_c_fmt_scan = ir.Constant(ir.ArrayType(ir.IntType(8), len(float_fmt_scan)),
                                     bytearray(float_fmt_scan.encode("utf8")))
        self.float_global_fmt_scan = ir.GlobalVariable(
            self.module, flo_c_fmt_scan.type, name="fstr_float_scan")
        self.float_global_fmt_scan.linkage = 'internal'
        self.float_global_fmt_scan.align = 4
        self.float_global_fmt_scan.initializer = flo_c_fmt_scan

        int_fmt = "%i\n\0"
        int_c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(int_fmt)),
                                bytearray(int_fmt.encode("utf8")))
        self.int_global_fmt = ir.GlobalVariable(
            self.module, int_c_fmt.type, name="fstr_int")
        self.int_global_fmt.linkage = 'internal'
        self.int_global_fmt.align = 4
        self.int_global_fmt.initializer = int_c_fmt

        float_fmt = "%f\n\0"
        flo_c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(float_fmt)),
                                bytearray(float_fmt.encode("utf8")))
        self.float_global_fmt = ir.GlobalVariable(
            self.module, flo_c_fmt.type, name="fstr_float")
        self.float_global_fmt.linkage = 'internal'
        self.float_global_fmt.align = 4
        self.float_global_fmt.initializer = flo_c_fmt

    def _declare_read_function(self):
        self.voidptr_ty = ir.IntType(8).as_pointer()
        scanf_ty = ir.FunctionType(ir.IntType(
            32), [self.voidptr_ty], var_arg=True)
        scanf = ir.Function(self.module, scanf_ty, name="__isoc99_scanf")
        self.scanf = scanf

        int_fmt_scan = "%i\0"
        int_c_fmt_scan = ir.Constant(ir.ArrayType(ir.IntType(8), len(int_fmt_scan)),
                                     bytearray(int_fmt_scan.encode("utf8")))
        self.int_global_fmt_scan = ir.GlobalVariable(
            self.module, int_c_fmt_scan.type, name="fstr_int_scan")
        self.int_global_fmt_scan.linkage = 'internal'
        self.int_global_fmt_scan.align = 4
        self.int_global_fmt_scan.initializer = int_c_fmt_scan

        float_fmt_scan = "%f\0"
        flo_c_fmt_scan = ir.Constant(ir.ArrayType(ir.IntType(8), len(float_fmt_scan)),
                                     bytearray(float_fmt_scan.encode("utf8")))
        self.float_global_fmt_scan = ir.GlobalVariable(
            self.module, flo_c_fmt_scan.type, name="fstr_float_scan")
        self.float_global_fmt_scan.linkage = 'internal'
        self.float_global_fmt_scan.align = 4
        self.float_global_fmt_scan.initializer = flo_c_fmt_scan

        # self.int_scan_arg = self.builder.bitcast(self.int_global_fmt_scan, self.voidptr_ty)
        # self.float_scan_arg = self.builder.bitcast(self.float_global_fmt_scan, self.voidptr_ty)

    def _declare_print_functions(self):
        self.voidptr_ty = ir.IntType(8).as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(
            32), [self.voidptr_ty], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name="printf")
        self.printf = printf

        int_fmt = "%i\n\0"
        int_c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(int_fmt)),
                                bytearray(int_fmt.encode("utf8")))
        self.int_global_fmt = ir.GlobalVariable(
            self.module, int_c_fmt.type, name="fstr_int")
        self.int_global_fmt.linkage = 'internal'
        self.int_global_fmt.align = 4
        self.int_global_fmt.initializer = int_c_fmt

        float_fmt = "%f\n\0"
        flo_c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(float_fmt)),
                                bytearray(float_fmt.encode("utf8")))
        self.float_global_fmt = ir.GlobalVariable(
            self.module, flo_c_fmt.type, name="fstr_float")
        self.float_global_fmt.linkage = 'internal'
        self.float_global_fmt.align = 4
        self.float_global_fmt.initializer = flo_c_fmt

        # self.int_print_arg = self.builder.bitcast(self.int_global_fmt, self.voidptr_ty)
        # self.float_print_arg = self.builder.bitcast(self.float_global_fmt, self.voidptr_ty)

    def _compile_ir(self):
        llvm_ir = str(self.module)
        print(llvm_ir)
        mod = self.binding.parse_assembly(llvm_ir)
        mod.verify()
        self.engine.add_module(mod)
        self.engine.finalize_object()
        self.engine.run_static_constructors()
        return mod

    def _gen_code_types(self, var):
        if type(var) == int:
            num = ir.Constant(ir.IntType(32), var)
            return num
        elif type(var) == float:
            num = ir.Constant(ir.FloatType(), var)
            return num
        else:
            load = self.builder.load(var)
            return load

    def create_ir(self):
        self._compile_ir()

    def save_ir(self, filename):
        with open(filename, 'w') as output_file:
            output_file.write(str(self.module))

    def get_scope(self, node, return_node=False):
        scope = None
        scope_node = None
        if ': Programa' in node.parent.name:
            scope = 'global'
        if ': declaracao_funcao' in node.parent.name:
            for child in node.children:
                if ': ID' in child.name:
                    scope = child.children[0].name.split(' ')[1]
                    scope_node = child
                    break
        if scope:
            if return_node:
                return scope, scope_node
            else:
                return scope
        return self.get_scope(node.parent, return_node)

    def get_type(self, node):
        if ': variavel' in node.name:
            return self.get_type(node.children[0])
        if ': NUM_INTEIRO' in node.name:
            return 'INTEIRO'
        if ': NUM_PONTO_FLUTUANTE' in node.name:
            return 'FLUTUANTE'
        if ': ID' in node.name:
            return self.symbol_table[node.name]['type']
        if ': chamada_funcao' in node.name:
            return self.symbol_table[node.children[0].name]['type']
        return None

    def cg_variable_declaration(self, scope):
        for symbol in self.symbol_table:
            if self.symbol_table[symbol]['scope'] == scope:
                if self.symbol_table[symbol]['ID_type'] == 'declaration':
                    label = self.symbol_table[symbol]['label'] + '_' + scope

                    if self.symbol_table[symbol]['type'] == 'INTEIRO':
                        var_tp = ir.IntType(32)
                        if self.symbol_table[symbol]['index']:
                            var_tp = ir.ArrayType(ir.IntType(
                                32), self.symbol_table[symbol]['size'])

                        var = self.builder.alloca(var_tp, name=label)
                        var.align = 4

                        if not self.symbol_table[symbol]['index']:
                            self.builder.store(self.intInitializer, var)

                    elif self.symbol_table[symbol]['type'] == 'FLUTUANTE':
                        var_tp = ir.FloatType()
                        if self.symbol_table[symbol]['index']:
                            var_tp = ir.ArrayType(
                                ir.FloatType(), self.symbol_table[symbol]['size'])

                        var = self.builder.alloca(var_tp, name=label)
                        var.align = 4

                        if not self.symbol_table[symbol]['index']:
                            self.builder.store(self.floatInitializer, var)

                    self.variables.append(var)

    def search_variables(self, var):

        for v in self.variables:
            if v.name == str(var):
                return v
        for gv in self.globalVariables:
            if gv.name == str(var):
                return gv

        return None

    def search_arguments(self, var):

        for a in self.args:
            if a[1] == str(var):
                return a[0]
        return None

    def search_functions(self, func):
        for f in self.functions:
            if f.name == str(func):
                return f
        return None

    def load_var(self, var):
        if type(var) == int:
            num = ir.Constant(ir.IntType(32), var)
            return num
        elif type(var) == float:
            num = ir.Constant(ir.FloatType(), var)
            return num
        elif 'i32*' in str(var.type) or 'float*' in str(var.type):
            load = self.builder.load(var)
            return load
        elif hasattr(var, 'type'):
            return var
        elif isinstance(var, ir.Instruction):
            return var

    def resolve_bin_op(self, op, has_neg=False):
        logging.debug('Resolving bin op...')
        if not has_neg:
            var1 = self.load_var(op[0])
            operation = op[1]
            var2 = self.load_var(op[2])
        elif has_neg:
            operation = op[0]
            var2 = self.load_var(op[1])

        print('OPERACAO ==> ', operation)

        # Math operations
        if operation == '+':
            if 'i32' in str(var1.type) and 'i32' in str(var2.type):
                var1 = self.builder.ptrtoint(var1, ir.IntType(32))
                var2 = self.builder.ptrtoint(var2, ir.IntType(32))
                temp = self.builder.add(var1, var2, name='tempadd')
            else:
                temp = self.builder.fadd(var1, var2, name='tempadd')

        elif operation == '-':
            if 'i32' in str(var1.type) and 'i32' in str(var2.type):
                var1 = self.builder.ptrtoint(var1, ir.IntType(32))
                var2 = self.builder.ptrtoint(var2, ir.IntType(32))
                temp = self.builder.sub(var1, var2, name='tempsub')
            else:
                temp = self.builder.fsub(var1, var2, name='tempsub')

        elif operation == '/':
            if 'i32' in str(var1.type) and 'i32' in str(var2.type):
                var1 = self.builder.ptrtoint(var1, ir.IntType(32))
                var2 = self.builder.ptrtoint(var2, ir.IntType(32))
                temp = self.builder.udiv(var1, var2, name='tempdiv')
            else:
                temp = self.builder.fdiv(var1, var2, name='tempdiv')

        elif operation == '*':
            if 'i32' in str(var1.type) and 'i32' in str(var2.type):
                var1 = self.builder.ptrtoint(var1, ir.IntType(32))
                var2 = self.builder.ptrtoint(var2, ir.IntType(32))
                temp = self.builder.mul(var1, var2, name='tempmul')
            else:
                temp = self.builder.fmul(var1, var2, name='tempmul')

        # Relational operations
        elif operation == '=':
            if 'i32' in str(var1.type) and 'i32' in str(var2.type):
                var1 = self.builder.ptrtoint(var1, ir.IntType(32))
                var2 = self.builder.ptrtoint(var2, ir.IntType(32))
                temp = self.builder.icmp_signed(
                    '==', var1, var2, name='tempcmp')
            else:
                temp = self.builder.fcmp_ordered(
                    '==', var1, var2, name='tempcmp')
        elif operation == '<>':
            if 'i32' in str(var1.type) and 'i32' in str(var2.type):
                var1 = self.builder.ptrtoint(var1, ir.IntType(32))
                var2 = self.builder.ptrtoint(var2, ir.IntType(32))
                temp = self.builder.icmp_signed(
                    '!=', var1, var2, name='tempcmp')
            else:
                temp = self.builder.fcmp_ordered(
                    '!=', var1, var2, name='tempcmp')
        elif operation == '>=':
            if 'i32' in str(var1.type) and 'i32' in str(var2.type):
                var1 = self.builder.ptrtoint(var1, ir.IntType(32))
                var2 = self.builder.ptrtoint(var2, ir.IntType(32))
                temp = self.builder.icmp_signed(
                    '>=', var1, var2, name='tempcmp')
            else:
                temp = self.builder.fcmp_ordered(
                    '>=', var1, var2, name='tempcmp')
        elif operation == '<=':
            if 'i32' in str(var1.type) and 'i32' in str(var2.type):
                var1 = self.builder.ptrtoint(var1, ir.IntType(32))
                var2 = self.builder.ptrtoint(var2, ir.IntType(32))
                temp = self.builder.icmp_signed(
                    '<=', var1, var2, name='tempcmp')
            else:
                temp = self.builder.fcmp_ordered(
                    '<=', var1, var2, name='tempcmp')
        elif operation == '>':
            if 'i32' in str(var1.type) and 'i32' in str(var2.type):
                var1 = self.builder.ptrtoint(var1, ir.IntType(32))
                var2 = self.builder.ptrtoint(var2, ir.IntType(32))
                temp = self.builder.icmp_signed(
                    '>', var1, var2, name='tempcmp')
            else:
                temp = self.builder.fcmp_ordered(
                    '>', var1, var2, name='tempcmp')
        elif operation == '<':
            if 'i32' in str(var1.type) and 'i32' in str(var2.type):
                var1 = self.builder.ptrtoint(var1, ir.IntType(32))
                var2 = self.builder.ptrtoint(var2, ir.IntType(32))
                temp = self.builder.icmp_signed(
                    '<', var1, var2, name='tempcmp')
            else:
                temp = self.builder.fcmp_ordered(
                    '<', var1, var2, name='tempcmp')

        # Logical operations
        elif operation == '&&':
            if 'i32' in str(var1.type) and 'i32' in str(var2.type):
                var1 = self.builder.ptrtoint(var1, ir.IntType(32))
                var2 = self.builder.ptrtoint(var2, ir.IntType(32))

            with self.builder.if_else(var1) as (then, otherwise):
                with then:
                    temp = var2
                with otherwise:
                    temp = var1

        elif operation == '||':
            if 'i32' in str(var1.type) and 'i32' in str(var2.type):
                var1 = self.builder.ptrtoint(var1, ir.IntType(32))
                var2 = self.builder.ptrtoint(var2, ir.IntType(32))

            with self.builder.if_else(var1) as (then, otherwise):
                with then:
                    temp = var1
                with otherwise:
                    temp = var2

        elif operation == '!':
            if 'i32' in str(var2.type):
                var2 = self.builder.ptrtoint(var2, ir.IntType(32))
            temp = self.builder.neg(var2, name='tempneg')

        logging.debug("Result: '{}'".format(temp))
        return temp

    def get_element(self, node):
        var_name = node.children[0].name
        var = None
        if self.symbol_table[var_name]['scope'] != 'global':
            var = self.search_variables(
                self.symbol_table[var_name]['label'] + '_' + self.symbol_table[var_name]['scope'])
        if var == None:
            var = self.search_arguments(
                self.symbol_table[var_name]['label'])
        if var == None:
            var = self.search_variables(
                self.symbol_table[var_name]['label'])
        if var == None:
            raise ReferenceError("Variable not found")

        expressao_index = get_leaves_index(node.children[1].children[1])
        idx, until = self.resolves_parentheses(0, expressao_index)

        idx = self.load_var(idx)

        idx = self.builder.ptrtoint(idx, ir.IntType(32))

        gep = self.builder.gep(
            var, [self.intInitializer, self.intInitializer])
        assigned_vector = self.builder.gep(gep, [idx])
        return assigned_vector

    def resolve_expression(self, exp):
        logging.debug("Resolving expression...")
        op = []
        result_op = None
        has_negacao = False
        for e in exp:
            if ': chamada_funcao' in e.name:
                func_ret = self.cg_function_call(e)
                op.append(func_ret)
            elif ': variavel' in e.name:
                element = self.get_element(e)
                op.append(element)
            elif ': ID' in e.parent.name:
                if self.symbol_table[e.parent.name]['scope'] != 'global':
                    var = self.search_variables(
                        self.symbol_table[e.parent.name]['label'] + '_' + self.symbol_table[e.parent.name]['scope'])
                if var == None:
                    var = self.search_arguments(
                        self.symbol_table[e.parent.name]['label'])
                if var == None:
                    var = self.search_variables(
                        self.symbol_table[e.parent.name]['label'])
                if var == None:
                    raise ReferenceError("Variable not found")
                op.append(var)

            elif ': OPERADOR' in e.parent.name:
                if ': OPERADOR_NEGACAO' in e.parent.name:
                    has_negacao = True
                op.append(e.name.split(' ')[1])

            elif ': NUM_' in e.parent.name:
                num = None
                try:
                    num = int(e.name.split(' ')[1])
                except Exception as ex:
                    try:
                        num = float(e.name.split(' ')[1])
                    except Exception as ex:
                        pass
                if num == None:
                    raise ReferenceError("Invalid number")
                op.append(num)
            elif isinstance(e, ir.Instruction):
                op.append(e)

            if len(op) > 2 and not has_negacao:
                result_op = self.resolve_bin_op(op)
                op = []
                op.append(result_op)
            if len(op) == 2 and has_negacao:
                result_op = self.resolve_bin_op(op, has_neg=True)
                op = []
                op.append(result_op)
                has_negacao = False
        logging.debug("Result: {}".format(result_op))

        if len(exp) == 1:
            result_op = self.load_var(op[0])

        return result_op

    def resolves_parentheses(self, pos, leaves):
        logging.debug("Resolving parantheses...")
        op = []
        popped_indexes = []
        for i in range(pos, len(leaves)):
            if i in popped_indexes:
                continue
            else:
                if ': ABRE' not in leaves[i].name and ': FECHA' not in leaves[i].name:
                    op.append(leaves[i])
                if ': ABRE' in leaves[i].name:
                    resolved, until = self.resolves_parentheses(i+1, leaves)
                    if resolved:
                        op.append(resolved)
                    if until:
                        for j in range(i+1, until+1):
                            if j < len(leaves):
                                popped_indexes.append(j)
                            else:
                                break
                if ': FECHA' in leaves[i].name:
                    resolved = self.resolve_expression(op)
                    logging.debug("Result: {}".format(resolved))
                    return resolved, i
        result = self.resolve_expression(op)
        logging.debug("Result: {}".format(result))
        return result, None

    def cg_assignment(self, node):
        logging.debug("Resolving assignment")
        variavel = node.children[0].children[0]
        expressao = node.children[2]

        if self.symbol_table[variavel.name]['scope'] != 'global':
            var = self.search_variables(
                self.symbol_table[variavel.name]['label'] + '_' + self.symbol_table[variavel.name]['scope'])
        if var == None:
            var = self.search_arguments(
                self.symbol_table[variavel.name]['label'])
        if var == None:
            var = self.search_variables(
                self.symbol_table[variavel.name]['label'])
        if var == None:
            raise ReferenceError("Varible not found")

        leaves = get_leaves(expressao)
        resolved, until = self.resolves_parentheses(0, leaves)

        if 'float' in str(resolved.type) and 'i32' in str(var.type):
            resolved = self.builder.fptosi(resolved, ir.IntType(32))
        elif 'i32' in str(resolved.type) and 'float' in str(var.type):
            resolved = self.builder.sitofp(resolved, ir.FloatType())

        if self.symbol_table[variavel.name]['index']:
            if hasattr(self.symbol_table[variavel.name]['size'], 'is_leaf'):
                expressao_index = get_leaves(
                    self.symbol_table[variavel.name]['size'])
                idx, until = self.resolves_parentheses(0, expressao_index)
            elif type(self.symbol_table[variavel.name]['size']) == int:
                idx = self.symbol_table[variavel.name]['size']

            var = self.load_var(var)
            idx = self.load_var(idx)

            idx = self.builder.ptrtoint(idx, ir.IntType(32))

            gep = self.builder.gep(
                var, [self.intInitializer, self.intInitializer])
            assigned_vector = self.builder.gep(gep, [idx])

            self.builder.store(resolved, assigned_vector)
        else:
            try:
                self.builder.store(resolved, var)
            except Exception as e:
                try:
                    var = self.load_var(var)
                    self.builder.store(resolved, var)
                except Exception as ex:
                    logging.warning("Exception on store operation:\n\t{}\n\t{}".format(
                        e, ex
                    ))

        logging.debug("Assignment resolved...")

    def check_body(self, node, ID, if_body=False):
        fn_ret = None
        for child in node.children:
            if ': atribuicao' in child.name:
                self.cg_assignment(child)
            if ': chamada_funcao' in child.name:
                self.cg_function_call(child)
            if ': leia' in child.name:
                self.cg_read(child)
            if ': escreva' in child.name:
                self.cg_write(child)
            if ': se' in child.name:
                self.cg_conditional(child, ID)
            if ': repita' in child.name:
                self.cg_repeat(child, ID)
            if ': retorna' in child.name:
                fn_ret = self.cg_return(child, ID)

        if not fn_ret and not if_body:
            self.builder.ret_void()

    def fn_build_body(self, ID, declaration, node, if_body=False):
        self.variables = []

        self.args = []
        params = self.symbol_table[ID.name]['params']
        for k in range(len(declaration.args)):
            if 'i32' in str(declaration.args[k].type):
                var_tp = ir.IntType(32)
                var = self.builder.alloca(var_tp)
                var.align = 4
            if 'float' in str(declaration.args[k].type):
                var_tp = ir.FloatType()
                var = self.builder.alloca(var_tp)
                var.align = 4

            self.builder.store(declaration.args[k], var)
            self.args.append((var, params[k]['label']))

        self.cg_variable_declaration(self.symbol_table[ID.name]['label'])

        self.check_body(node, ID)

    def cg_function_declaration(self, node):
        tipo = None
        if len(node.children) > 1:
            if ': tipo' in node.children[0].name:
                tipo = node.children[0].children[0].name.split(' ')[1]
            header = node.children[1]
        else:
            header = node.children[0]

        for i in range(len(header.children)):
            if ': ID' in header.children[i].name:
                ID = header.children[i]
            if ': corpo' in header.children[i].name:
                fn_body = header.children[i]

        fn_args_tp = []
        for p in self.symbol_table[ID.name]['params']:
            if p['type'] == 'INTEIRO':
                fn_args_tp.append(ir.IntType(32))
            else:
                fn_args_tp.append(ir.FloatType())

        if tipo:
            if tipo == 'INTEIRO':
                fn_tp = ir.FunctionType(ir.IntType(32), fn_args_tp)
            elif tipo == 'FLUTUANTE':
                fn_tp = ir.FunctionType(ir.FloatType(), fn_args_tp)
        else:
            fn_tp = ir.FunctionType(ir.VoidType(), fn_args_tp)

        fn_name = self.symbol_table[ID.name]['label']
        if fn_name == 'principal':
            fn_name = 'main'

        fn_declared = ir.Function(
            self.module, fn_tp, name=fn_name)
        self.functions.append(fn_declared)
        fn_block = fn_declared.append_basic_block(fn_name+'_entry')
        self.builder = ir.IRBuilder(fn_block)
        self.builder.goto_block(fn_block)
        self.fn_build_body(ID, fn_declared, fn_body)

    def cg_function_call(self, node):
        for child in node.children:
            if ': ID' in child.name:
                ID = node.children[0]
                break

        label = self.symbol_table[ID.name]['label']
        params = self.symbol_table[ID.name]['args_node']

        leaves = []

        call_args = []

        if len(params.children) == 1:
            leaves = get_leaves(params.children[0])
            if not leaves:
                leaves = get_leaves_index(params.children[0])
            result, until = self.resolves_parentheses(0, leaves)
            result = self.load_var(result)

            if 'i32' in str(result.type):
                result = self.builder.ptrtoint(result, ir.IntType(32))
            call_args.append(result)

        else:
            for p in params.children:
                if ': expressao' in p.name:
                    leaves = get_leaves(p)
                    if not leaves:
                        leaves = get_leaves_index(p)
                    result, until = self.resolves_parentheses(0, leaves)
                    result = self.load_var(result)
                    if 'i32' in str(result.type):
                        result = self.builder.ptrtoint(result, ir.IntType(32))
                    call_args.append(result)

        if not leaves:
            leaves = get_leaves_index(params.children[0])
            result, until = self.resolves_parentheses(0, leaves)
            result = self.load_var(result)
            if 'i32' in str(result.type):
                result = self.builder.ptrtoint(result, ir.IntType(32))
            call_args.append(result)

        call_func = self.search_functions(label)
        func_ret = self.builder.call(call_func, call_args)
        return func_ret

    def cg_write(self, node):
        expressao = node.children[2]

        leaves = get_leaves(expressao)

        result, until = self.resolves_parentheses(0, leaves)

        result = self.load_var(result)

        self.int_print_arg = self.builder.bitcast(
            self.int_global_fmt, self.voidptr_ty)
        self.float_print_arg = self.builder.bitcast(
            self.float_global_fmt, self.voidptr_ty)

        if 'i32' in str(result.type):
            self.builder.call(
                self.printf, [self.int_print_arg, result])
        else:
            double = self.builder.fpext(result, ir.DoubleType())
            self.builder.call(
                self.printf, [self.float_print_arg, double])

    def cg_read(self, node):
        expressao = node.children[2]
        var = None
        var_name = expressao.children[0].name
        if ': ID' in var_name:
            if self.symbol_table[var_name]['scope'] != 'global':
                var = self.search_variables(
                    self.symbol_table[var_name]['label'] + '_' + self.symbol_table[var_name]['scope'])
            if var == None:
                var = self.search_arguments(
                    self.symbol_table[var_name]['label'])
            if var == None:
                var = self.search_variables(
                    self.symbol_table[var_name]['label'])
            if var == None:
                raise ReferenceError("Variable not found")

        result = var

        self.int_scan_arg = self.builder.bitcast(
            self.int_global_fmt_scan, self.voidptr_ty)
        self.float_scan_arg = self.builder.bitcast(
            self.float_global_fmt_scan, self.voidptr_ty)

        if 'i32' in str(result.type):
            self.builder.call(
                self.scanf, [self.int_scan_arg, result])
        else:
            self.builder.call(
                self.scanf, [self.float_scan_arg, result])

    def cg_return(self, node, ID):
        logging.debug("Resolving return statment...")

        expressao = node.children[2]

        leaves = get_leaves(expressao)

        returned, until = self.resolves_parentheses(0, leaves)

        if 'i32' in str(returned):
            returned = self.builder.ptrtoint(returned, ir.IntType(32))

        self.builder.ret(returned)

        logging.debug("Retorned value: {}".format(returned))
        return returned

    def cg_repeat(self, node, ID):

        repeat_block = self.builder.append_basic_block(name='repeat')
        end_repeat = self.builder.append_basic_block(name='repeat_end')

        self.builder.branch(repeat_block)
        self.builder.position_at_start(repeat_block)
        self.check_body(node.children[1], ID, if_body=True)

        leaves = get_leaves(node.children[3])
        result, until = self.resolves_parentheses(0, leaves)
        self.builder.cbranch(result, end_repeat, repeat_block)
        self.builder.position_at_start(end_repeat)

    def cg_conditional(self, node, ID):
        leaves = get_leaves(node.children[1])
        result, until = self.resolves_parentheses(0, leaves)

        if len(node.children) == 5:
            with self.builder.if_then(result):
                self.check_body(node.children[3], ID, if_body=True)
        if len(node.children) == 7:
            with self.builder.if_else(result) as (then, otherwise):
                with then:
                    self.check_body(node.children[3], ID, if_body=True)
                with otherwise:
                    self.check_body(node.children[5], ID, if_body=True)

    def cg_global_variables(self):
        for symbol in self.symbol_table:
            if self.symbol_table[symbol]['scope'] == 'global':
                if self.symbol_table[symbol]['ID_type'] == 'declaration':
                    label = self.symbol_table[symbol]['label']

                    if self.symbol_table[symbol]['type'] == 'INTEIRO':
                        var_tp = ir.IntType(32)
                        zeros = ir.Constant(
                            ir.IntType(32), 0)
                        if self.symbol_table[symbol]['index']:
                            size = self.symbol_table[symbol]['size']
                            var_tp = ir.ArrayType(ir.IntType(
                                32), size)

                            zeros = ir.Constant(ir.ArrayType(
                                ir.IntType(32), size), None)

                        globalVar = ir.GlobalVariable(
                            self.module, var_tp, label)
                        globalVar.initializer = zeros

                    elif self.symbol_table[symbol]['type'] == 'FLUTUANTE':
                        var_tp = ir.FloatType()
                        zeros = ir.Constant(
                            ir.FloatType(), 0)
                        if self.symbol_table[symbol]['index']:
                            size = self.symbol_table[symbol]['size']
                            var_tp = ir.ArrayType(ir.FloatType(), size)

                            zeros = ir.Constant(ir.ArrayType(
                                ir.FloatType(), size), None)

                        globalVar = ir.GlobalVariable(
                            self.module, var_tp, label)
                        globalVar.initializer = zeros

                    globalVar.linkage = 'common'
                    globalVar.align = 4

                    self.globalVariables.append(globalVar)

    def coge_generation(self):

        self.cg_global_variables()

        queue = list(PreOrderIter(self.root))
        while queue:
            node = queue.pop(0)
            if not node.is_leaf and node.parent:
                scope = self.get_scope(node)
                if ': declaracao_funcao' in node.name:
                    self.cg_function_declaration(node)


def main(logging_level, export_AST=False):
    try:
        root, symbol_table, has_semantic_error = semantic.main(
            logging_level, True)
        if has_semantic_error:
            raise SemanticError("Semantic Errors found")
        if not root:
            pass
        if root and not root.is_leaf:
            pass
    except SemanticError as e:
        has_semantic_error = True
        logging.error("Unable to generate code -- Fix Semantic Errors")
        exit(1)

    file_name = argv[1].split('/')[-1]
    file_name = file_name.split('.')[0]
    file_name = file_name+".ll"

    cg = CodeGen(root, symbol_table, file_name)
    cg.coge_generation()
    cg.create_ir()

    cg.save_ir("./output_ll/"+file_name)

    fn_ptr = cg.engine.get_function_address('main')

    c_fn = CFUNCTYPE(c_int)(fn_ptr)
    res = c_fn()

    print('\n\nReturning ==> {}'.format(str(res)))


if __name__ == '__main__':
    main(logging.DEBUG, True)
