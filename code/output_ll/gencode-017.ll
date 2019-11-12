; ModuleID = "gencode-017.ll"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"__isoc99_scanf"(i8* %".1", ...) 

declare i32 @"printf"(i8* %".1", ...) 

@"fstr_int_scan" = internal global [3 x i8] c"%i\00", align 4
@"fstr_float_scan" = internal global [3 x i8] c"%f\00", align 4
@"fstr_int" = internal global [4 x i8] c"%i\0a\00", align 4
@"fstr_float" = internal global [4 x i8] c"%f\0a\00", align 4
define i32 @"main"() 
{
main_entry:
  %"x_principal" = alloca i32, align 4
  store i32 0, i32* %"x_principal"
  %"y_principal" = alloca float, align 4
  store float              0x0, float* %"y_principal"
  store i32 0, i32* %"x_principal"
  store float              0x0, float* %"y_principal"
  %".6" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".7" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".8" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".6", i32* %"x_principal")
  %".9" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".10" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".11" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".10", float* %"y_principal")
  %".12" = load i32, i32* %"x_principal"
  %".13" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".14" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".15" = call i32 (i8*, ...) @"printf"(i8* %".13", i32 %".12")
  %".16" = load float, float* %"y_principal"
  %".17" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".18" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".19" = fpext float %".16" to double
  %".20" = call i32 (i8*, ...) @"printf"(i8* %".18", double %".19")
  ret i32 0
}
