; ModuleID = "code_generation.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"__isoc99_scanf"(i8* %".1", ...) 

declare i32 @"printf"(i8* %".1", ...) 

@"fstr_int_scan" = internal global [3 x i8] c"%i\00", align 4
@"fstr_float_scan" = internal global [3 x i8] c"%f\00", align 4
@"fstr_int" = internal global [4 x i8] c"%i\0a\00", align 4
@"fstr_float" = internal global [4 x i8] c"%f\0a\00", align 4
@"n" = common global i32 0, align 4
@"soma" = common global i32 0, align 4
define i32 @"main"() 
{
main_entry:
  store i32 10, i32* @"n"
  store i32 0, i32* @"soma"
  br label %"repeat"
repeat:
  %".5" = load i32, i32* @"soma"
  %".6" = load i32, i32* @"n"
  %"tempadd" = add i32 %".5", %".6"
  store i32 %"tempadd", i32* @"soma"
  %".8" = load i32, i32* @"n"
  %"tempsub" = sub i32 %".8", 1
  store i32 %"tempsub", i32* @"n"
  %".10" = load i32, i32* @"n"
  %"tempcmp" = icmp eq i32 %".10", 0
  br i1 %"tempcmp", label %"repeat", label %"repeat_end"
repeat_end:
  ret i32 0
}
