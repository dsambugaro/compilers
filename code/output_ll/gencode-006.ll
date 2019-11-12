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
  %"tempadd" = add i32 %".1", %".2"
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
  %"i_principal" = alloca i32, align 4
  store i32 0, i32* %"i_principal"
  store i32 0, i32* %"i_principal"
  br label %"repeat"
repeat:
  %".8" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".9" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".10" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".8", i32* %"a_principal")
  %".11" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".12" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".13" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".11", i32* %"b_principal")
  %".14" = load i32, i32* %"a_principal"
  %".15" = load i32, i32* %"b_principal"
  %".16" = call i32 @"soma"(i32 %".14", i32 %".15")
  store i32 %".16", i32* %"c_principal"
  %".18" = load i32, i32* %"c_principal"
  %".19" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".20" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".21" = call i32 (i8*, ...) @"printf"(i8* %".19", i32 %".18")
  %".22" = load i32, i32* %"i_principal"
  %"tempadd" = add i32 %".22", 1
  store i32 %"tempadd", i32* %"i_principal"
  %".24" = load i32, i32* %"i_principal"
  %"tempcmp" = icmp eq i32 %".24", 5
  br i1 %"tempcmp", label %"repeat", label %"repeat_end"
repeat_end:
  ret i32 0
}
