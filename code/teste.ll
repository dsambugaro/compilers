; ModuleID = "code_generation.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"__isoc99_scanf"(i8* %".1", ...) 

declare i32 @"printf"(i8* %".1", ...) 

@"fstr_int_scan" = internal global [3 x i8] c"%i\00", align 4
@"fstr_float_scan" = internal global [3 x i8] c"%f\00", align 4
@"fstr_int" = internal global [4 x i8] c"%i\0a\00", align 4
@"fstr_float" = internal global [4 x i8] c"%f\0a\00", align 4
@"A" = common global [1024 x i32] zeroinitializer, align 4
@"B" = common global [1024 x i32] zeroinitializer, align 4
define i32 @"main"() 
{
main_entry:
  %"a_principal" = alloca i32, align 4
  store i32 0, i32* %"a_principal"
  %"i_principal" = alloca i32, align 4
  store i32 0, i32* %"i_principal"
  store i32 0, i32* %"i_principal"
  br label %"repeat"
repeat:
  %".6" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".7" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".8" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".6", i32* %"a_principal")
  %".9" = load i32, i32* %"a_principal"
  %".10" = load i32, i32* %"a_principal"
  %".11" = getelementptr [1024 x i32], [1024 x i32]* @"A", i32 0, i32 0
  %".12" = getelementptr i32, i32* %".11", i32 %".10"
  store i32 %".9", i32* %".12"
  %".14" = load i32, i32* %"i_principal"
  %"tempadd" = add i32 %".14", 1
  store i32 %"tempadd", i32* %"i_principal"
  %".16" = load i32, i32* %"i_principal"
  %"tempcmp" = icmp eq i32 %".16", 1024
  br i1 %"tempcmp", label %"repeat", label %"repeat_end"
repeat_end:
  br label %"repeat.1"
repeat.1:
  %".19" = load i32, i32* %"i_principal"
  %".20" = getelementptr [1024 x i32], [1024 x i32]* @"A", i32 0, i32 0
  %".21" = getelementptr i32, i32* %".20", i32 %".19"
  %".22" = load i32, i32* %".21"
  %".23" = load i32, i32* %"i_principal"
  %".24" = getelementptr [1024 x i32], [1024 x i32]* @"A", i32 0, i32 0
  %".25" = getelementptr i32, i32* %".24", i32 %".23"
  %".26" = load i32, i32* %".25"
  %".27" = getelementptr [1024 x i32], [1024 x i32]* @"B", i32 0, i32 0
  %".28" = getelementptr i32, i32* %".27", i32 %".26"
  store i32 %".22", i32* %".28"
  %".30" = load i32, i32* %"i_principal"
  %"tempadd.1" = add i32 %".30", 1
  store i32 %"tempadd.1", i32* %"i_principal"
  %".32" = load i32, i32* %"i_principal"
  %"tempcmp.1" = icmp eq i32 %".32", 1024
  br i1 %"tempcmp.1", label %"repeat.1", label %"repeat_end.1"
repeat_end.1:
  br label %"repeat.2"
repeat.2:
  %".35" = load i32, i32* %"i_principal"
  %".36" = getelementptr [1024 x i32], [1024 x i32]* @"B", i32 0, i32 0
  %".37" = getelementptr i32, i32* %".36", i32 %".35"
  %".38" = load i32, i32* %".37"
  %".39" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".40" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".41" = call i32 (i8*, ...) @"printf"(i8* %".39", i32 %".38")
  %".42" = load i32, i32* %"i_principal"
  %"tempadd.2" = add i32 %".42", 1
  store i32 %"tempadd.2", i32* %"i_principal"
  %".44" = load i32, i32* %"i_principal"
  %"tempcmp.2" = icmp eq i32 %".44", 1024
  br i1 %"tempcmp.2", label %"repeat.2", label %"repeat_end.2"
repeat_end.2:
  ret i32 0
}
