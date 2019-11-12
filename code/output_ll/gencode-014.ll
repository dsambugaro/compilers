; ModuleID = "gencode-014.ll"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"__isoc99_scanf"(i8* %".1", ...) 

declare i32 @"printf"(i8* %".1", ...) 

@"fstr_int_scan" = internal global [3 x i8] c"%i\00", align 4
@"fstr_float_scan" = internal global [3 x i8] c"%f\00", align 4
@"fstr_int" = internal global [4 x i8] c"%i\0a\00", align 4
@"fstr_float" = internal global [4 x i8] c"%f\0a\00", align 4
define i32 @"fibonacciRec"(i32 %".1") 
{
fibonacciRec_entry:
  %".3" = alloca i32, align 4
  store i32 %".1", i32* %".3"
  %".5" = load i32, i32* %".3"
  %"tempcmp" = icmp sle i32 %".5", 1
  br i1 %"tempcmp", label %"fibonacciRec_entry.if", label %"fibonacciRec_entry.else"
fibonacciRec_entry.if:
  %".7" = load i32, i32* %".3"
  ret i32 %".7"
fibonacciRec_entry.else:
  %".9" = load i32, i32* %".3"
  %".10" = call i32 @"fibonacciRec"(i32 %".9")
  %".11" = load i32, i32* %".3"
  %".12" = call i32 @"fibonacciRec"(i32 %".11")
  %"tempadd" = add i32 %".10", %".12"
  ret i32 %"tempadd"
fibonacciRec_entry.endif:
  ret i32 0
}

define i32 @"fibonacciIter"(i32 %".1") 
{
fibonacciIter_entry:
  %".3" = alloca i32, align 4
  store i32 %".1", i32* %".3"
  %"i_fibonacciIter" = alloca i32, align 4
  store i32 0, i32* %"i_fibonacciIter"
  %"f_fibonacciIter" = alloca i32, align 4
  store i32 0, i32* %"f_fibonacciIter"
  %"k_fibonacciIter" = alloca i32, align 4
  store i32 0, i32* %"k_fibonacciIter"
  store i32 1, i32* %"i_fibonacciIter"
  store i32 0, i32* %"f_fibonacciIter"
  store i32 1, i32* %"k_fibonacciIter"
  br label %"repeat"
repeat:
  %".12" = load i32, i32* %"i_fibonacciIter"
  %".13" = load i32, i32* %"f_fibonacciIter"
  %"tempadd" = add i32 %".12", %".13"
  store i32 %"tempadd", i32* %"f_fibonacciIter"
  %".15" = load i32, i32* %"f_fibonacciIter"
  %".16" = load i32, i32* %"i_fibonacciIter"
  %"tempsub" = sub i32 %".15", %".16"
  store i32 %"tempsub", i32* %"i_fibonacciIter"
  %".18" = load i32, i32* %"k_fibonacciIter"
  %"tempadd.1" = add i32 %".18", 1
  store i32 %"tempadd.1", i32* %"k_fibonacciIter"
  %".20" = load i32, i32* %"k_fibonacciIter"
  %".21" = load i32, i32* %".3"
  %"tempcmp" = icmp sle i32 %".20", %".21"
  br i1 %"tempcmp", label %"repeat_end", label %"repeat"
repeat_end:
  %".23" = load i32, i32* %"f_fibonacciIter"
  ret i32 %".23"
}

define i32 @"main"() 
{
main_entry:
  %"n_principal" = alloca i32, align 4
  store i32 0, i32* %"n_principal"
  %"i_principal" = alloca i32, align 4
  store i32 0, i32* %"i_principal"
  %".4" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".5" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".6" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".4", i32* %"n_principal")
  store i32 1, i32* %"i_principal"
  br label %"repeat"
repeat:
  %".9" = load i32, i32* %"i_principal"
  %".10" = call i32 @"fibonacciIter"(i32 %".9")
  %".11" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".12" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".11", i32 %".10")
  %".14" = load i32, i32* %"i_principal"
  %"tempadd" = add i32 %".14", 1
  store i32 %"tempadd", i32* %"i_principal"
  %".16" = load i32, i32* %"i_principal"
  %".17" = load i32, i32* %"n_principal"
  %"tempcmp" = icmp slt i32 %".16", %".17"
  br i1 %"tempcmp", label %"repeat_end", label %"repeat"
repeat_end:
  store i32 1, i32* %"i_principal"
  br label %"repeat.1"
repeat.1:
  %".21" = load i32, i32* %"i_principal"
  %".22" = call i32 @"fibonacciRec"(i32 %".21")
  %".23" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".24" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".25" = call i32 (i8*, ...) @"printf"(i8* %".23", i32 %".22")
  %".26" = load i32, i32* %"i_principal"
  %"tempadd.1" = add i32 %".26", 1
  store i32 %"tempadd.1", i32* %"i_principal"
  %".28" = load i32, i32* %"i_principal"
  %".29" = load i32, i32* %"n_principal"
  %"tempcmp.1" = icmp slt i32 %".28", %".29"
  br i1 %"tempcmp.1", label %"repeat_end.1", label %"repeat.1"
repeat_end.1:
  ret i32 0
}
