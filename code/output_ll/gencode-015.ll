; ModuleID = "gencode-015.ll"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"__isoc99_scanf"(i8* %".1", ...) 

declare i32 @"printf"(i8* %".1", ...) 

@"fstr_int_scan" = internal global [3 x i8] c"%i\00", align 4
@"fstr_float_scan" = internal global [3 x i8] c"%f\00", align 4
@"fstr_int" = internal global [4 x i8] c"%i\0a\00", align 4
@"fstr_float" = internal global [4 x i8] c"%f\0a\00", align 4
define i32 @"func"(i32 %".1", float %".2") 
{
func_entry:
  %".4" = alloca i32, align 4
  store i32 %".1", i32* %".4"
  %".6" = alloca float, align 4
  store float %".2", float* %".6"
  %"r_func" = alloca i32, align 4
  store i32 0, i32* %"r_func"
  %".9" = load i32, i32* %"r_func"
  ret i32 %".9"
}

define i32 @"main"() 
{
main_entry:
  %"x_principal" = alloca i32, align 4
  store i32 0, i32* %"x_principal"
  %".3" = call i32 @"func"(i32 1, float 0x4000000000000000)
  store i32 %".3", i32* %"x_principal"
  ret i32 0
}
