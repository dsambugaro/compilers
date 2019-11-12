; ModuleID = "code_generation.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"__isoc99_scanf"(i8* %".1", ...) 

declare i32 @"printf"(i8* %".1", ...) 

@"fstr_int_scan" = internal global [3 x i8] c"%i\00", align 4
@"fstr_float_scan" = internal global [3 x i8] c"%f\00", align 4
@"fstr_int" = internal global [4 x i8] c"%i\0a\00", align 4
@"fstr_float" = internal global [4 x i8] c"%f\0a\00", align 4
@"a" = common global i32 0, align 4
define i32 @"main"() 
{
main_entry:
  %"b_principal" = alloca i32, align 4
  store i32 0, i32* %"b_principal"
  store i32 10, i32* @"a"
  %".4" = load i32, i32* @"a"
  %"tempcmp" = icmp sge i32 %".4", 5
  %".5" = load i32, i32* @"a"
  %"tempcmp.1" = icmp sle i32 %".5", 20
  %"tempcond" = and i1 %"tempcmp", %"tempcmp.1"
  br i1 %"tempcond", label %"main_entry.if", label %"main_entry.else"
main_entry.if:
  store i32 50, i32* %"b_principal"
  br label %"main_entry.endif"
main_entry.else:
  store i32 100, i32* %"b_principal"
  br label %"main_entry.endif"
main_entry.endif:
  %".11" = load i32, i32* %"b_principal"
  %".12" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".13" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".14" = call i32 (i8*, ...) @"printf"(i8* %".12", i32 %".11")
  ret i32 0
}
