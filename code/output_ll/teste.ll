; ModuleID = "teste.ll"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"__isoc99_scanf"(i8* %".1", ...) 

declare i32 @"printf"(i8* %".1", ...) 

@"fstr_int_scan" = internal global [3 x i8] c"%i\00", align 4
@"fstr_float_scan" = internal global [3 x i8] c"%f\00", align 4
@"fstr_int" = internal global [4 x i8] c"%i\0a\00", align 4
@"fstr_float" = internal global [4 x i8] c"%f\0a\00", align 4
@"a" = common global i32 0, align 4
define i32 @"get"(i32 %".1") 
{
get_entry:
  %".3" = alloca i32, align 4
  store i32 %".1", i32* %".3"
  %".5" = load i32, i32* %".3"
  ret i32 %".5"
}

define i32 @"main"() 
{
main_entry:
  %"ret_principal" = alloca i32, align 4
  store i32 0, i32* %"ret_principal"
  %".3" = call i32 @"get"(i32 5)
  %".4" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".5" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".6" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %".3")
  store i32 10, i32* @"a"
  %".8" = call i32 @"get"(i32 9)
  %".9" = load i32, i32* @"a"
  %"tempcmp" = icmp eq i32 %".9", %".8"
  %".10" = call i32 @"get"(i32 10)
  %".11" = load i32, i32* @"a"
  %"tempcmp.1" = icmp eq i32 %".11", %".10"
  br i1 %"tempcmp", label %"main_entry.if", label %"main_entry.else"
main_entry.if:
  br label %"main_entry.endif"
main_entry.else:
  br label %"main_entry.endif"
main_entry.endif:
  br i1 %"tempcmp", label %"main_entry.endif.if", label %"main_entry.endif.else"
main_entry.endif.if:
  store i32 1, i32* %"ret_principal"
  br label %"main_entry.endif.endif"
main_entry.endif.else:
  store i32 0, i32* %"ret_principal"
  br label %"main_entry.endif.endif"
main_entry.endif.endif:
  %".20" = load i32, i32* %"ret_principal"
  ret i32 %".20"
}
