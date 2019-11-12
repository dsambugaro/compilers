; ModuleID = "gencode-012.ll"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"__isoc99_scanf"(i8* %".1", ...) 

declare i32 @"printf"(i8* %".1", ...) 

@"fstr_int_scan" = internal global [3 x i8] c"%i\00", align 4
@"fstr_float_scan" = internal global [3 x i8] c"%f\00", align 4
@"fstr_int" = internal global [4 x i8] c"%i\0a\00", align 4
@"fstr_float" = internal global [4 x i8] c"%f\0a\00", align 4
@"ano" = common global i32 0, align 4
define i32 @"modulo"(i32 %".1", i32 %".2") 
{
modulo_entry:
  %".4" = alloca i32, align 4
  store i32 %".1", i32* %".4"
  %".6" = alloca i32, align 4
  store i32 %".2", i32* %".6"
  %".8" = load i32, i32* %".4"
  %".9" = load i32, i32* %".6"
  %"tempcmp" = icmp slt i32 %".8", %".9"
  br i1 %"tempcmp", label %"modulo_entry.if", label %"modulo_entry.endif"
modulo_entry.if:
  %".11" = load i32, i32* %".4"
  ret i32 %".11"
modulo_entry.endif:
  br label %"repeat"
repeat:
  %".14" = load i32, i32* %".4"
  %".15" = load i32, i32* %".6"
  %"tempsub" = sub i32 %".14", %".15"
  store i32 %"tempsub", i32* %".4"
  %".17" = load i32, i32* %".4"
  %".18" = load i32, i32* %".6"
  %"tempcmp.1" = icmp sle i32 %".17", %".18"
  br i1 %"tempcmp.1", label %"repeat_end", label %"repeat"
repeat_end:
  %".20" = load i32, i32* %".4"
  ret i32 %".20"
}

define i32 @"main"() 
{
main_entry:
  %".2" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".3" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".4" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".2", i32* @"ano")
  %".5" = load i32, i32* @"ano"
  %".6" = call i32 @"modulo"(i32 %".5", i32 400)
  %"tempcmp" = icmp eq i32 %".6", 0
  %".7" = load i32, i32* @"ano"
  %".8" = call i32 @"modulo"(i32 %".7", i32 4)
  %"tempcmp.1" = icmp eq i32 %".8", 0
  %".9" = load i32, i32* @"ano"
  %".10" = call i32 @"modulo"(i32 %".9", i32 100)
  %"tempcmp.2" = icmp eq i32 %".10", 0
  %"tempneg" = sub i1 0, %"tempcmp.2"
  br i1 %"tempcmp.1", label %"main_entry.if", label %"main_entry.else"
main_entry.if:
  br label %"main_entry.endif"
main_entry.else:
  br label %"main_entry.endif"
main_entry.endif:
  br i1 %"tempcmp", label %"main_entry.endif.if", label %"main_entry.endif.else"
main_entry.endif.if:
  br label %"main_entry.endif.endif"
main_entry.endif.else:
  br label %"main_entry.endif.endif"
main_entry.endif.endif:
  br i1 %"tempcmp.1", label %"main_entry.endif.endif.if", label %"main_entry.endif.endif.endif"
main_entry.endif.endif.if:
  %".18" = load i32, i32* @"ano"
  %".19" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".20" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".21" = call i32 (i8*, ...) @"printf"(i8* %".19", i32 %".18")
  %".22" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".23" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".22", i32 1)
  br label %"main_entry.endif.endif.endif"
main_entry.endif.endif.endif:
  ret i32 0
}
