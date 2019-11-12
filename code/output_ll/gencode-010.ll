; ModuleID = "gencode-010.ll"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"__isoc99_scanf"(i8* %".1", ...) 

declare i32 @"printf"(i8* %".1", ...) 

@"fstr_int_scan" = internal global [3 x i8] c"%i\00", align 4
@"fstr_float_scan" = internal global [3 x i8] c"%f\00", align 4
@"fstr_int" = internal global [4 x i8] c"%i\0a\00", align 4
@"fstr_float" = internal global [4 x i8] c"%f\0a\00", align 4
@"n" = common global i32 0, align 4
define i32 @"fatorial"(i32 %".1") 
{
fatorial_entry:
  %".3" = alloca i32, align 4
  store i32 %".1", i32* %".3"
  %"fat_fatorial" = alloca i32, align 4
  store i32 0, i32* %"fat_fatorial"
  %".6" = load i32, i32* %".3"
  %"tempcmp" = icmp sgt i32 %".6", 0
  br i1 %"tempcmp", label %"fatorial_entry.if", label %"fatorial_entry.else"
fatorial_entry.if:
  store i32 1, i32* %"fat_fatorial"
  br label %"repeat"
fatorial_entry.else:
  ret i32 0
fatorial_entry.endif:
  ret i32 0
repeat:
  %".10" = load i32, i32* %"fat_fatorial"
  %".11" = load i32, i32* %".3"
  %"tempmul" = mul i32 %".10", %".11"
  store i32 %"tempmul", i32* %"fat_fatorial"
  %".13" = load i32, i32* %".3"
  %"tempsub" = sub i32 %".13", 1
  store i32 %"tempsub", i32* %".3"
  %".15" = load i32, i32* %".3"
  %"tempcmp.1" = icmp eq i32 %".15", 0
  br i1 %"tempcmp.1", label %"repeat_end", label %"repeat"
repeat_end:
  %".17" = load i32, i32* %"fat_fatorial"
  ret i32 %".17"
}

define i32 @"main"() 
{
main_entry:
  %".2" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".3" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".4" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".2", i32* @"n")
  %".5" = load i32, i32* @"n"
  %".6" = call i32 @"fatorial"(i32 %".5")
  %".7" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".8" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".7", i32 %".6")
  ret i32 0
}
