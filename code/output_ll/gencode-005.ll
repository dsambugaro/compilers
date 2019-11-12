; ModuleID = "code_generation.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"__isoc99_scanf"(i8* %".1", ...) 

declare i32 @"printf"(i8* %".1", ...) 

@"fstr_int_scan" = internal global [3 x i8] c"%i\00", align 4
@"fstr_float_scan" = internal global [3 x i8] c"%f\00", align 4
@"fstr_int" = internal global [4 x i8] c"%i\0a\00", align 4
@"fstr_float" = internal global [4 x i8] c"%f\0a\00", align 4
define i32 @"soma"(i32 %".1", i32 %".2") 
{
soma_entry:
  %".4" = alloca i32, align 4
  store i32 %".1", i32* %".4"
  %".6" = alloca i32, align 4
  store i32 %".2", i32* %".6"
  %".8" = load i32, i32* %".4"
  %".9" = load i32, i32* %".6"
  %"tempadd" = add i32 %".8", %".9"
  ret i32 %"tempadd"
}

define i32 @"main"() 
{
main_entry:
  %"a_principal" = alloca i32, align 4
  store i32 0, i32* %"a_principal"
  %"b_principal" = alloca i32, align 4
  store i32 0, i32* %"b_principal"
  %"c_principal" = alloca i32, align 4
  store i32 0, i32* %"c_principal"
  %".5" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".6" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".7" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".5", i32* %"a_principal")
  %".8" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".9" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".10" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".8", i32* %"b_principal")
  %".11" = load i32, i32* %"a_principal"
  %".12" = load i32, i32* %"b_principal"
  %".13" = call i32 @"soma"(i32 %".11", i32 %".12")
  store i32 %".13", i32* %"c_principal"
  %".15" = load i32, i32* %"c_principal"
  %".16" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".17" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".18" = call i32 (i8*, ...) @"printf"(i8* %".16", i32 %".15")
  ret i32 0
}
