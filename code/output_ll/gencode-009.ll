; ModuleID = "code_generation.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"__isoc99_scanf"(i8* %".1", ...) 

declare i32 @"printf"(i8* %".1", ...) 

@"fstr_int_scan" = internal global [3 x i8] c"%i\00", align 4
@"fstr_float_scan" = internal global [3 x i8] c"%f\00", align 4
@"fstr_int" = internal global [4 x i8] c"%i\0a\00", align 4
@"fstr_float" = internal global [4 x i8] c"%f\0a\00", align 4
@"A" = common global [1024 x float] zeroinitializer, align 4
@"B" = common global [1024 x float] zeroinitializer, align 4
@"C" = common global [1024 x float] zeroinitializer, align 4
define void @"somaVetores"(i32 %".1") 
{
somaVetores_entry:
  %"i_somaVetores" = alloca i32, align 4
  store i32 0, i32* %"i_somaVetores"
  store i32 0, i32* %"i_somaVetores"
  br label %"repeat"
repeat:
  %".6" = load i32, i32* %"i_somaVetores"
  %".7" = getelementptr [1024 x float], [1024 x float]* @"A", i32 0, i32 0
  %".8" = getelementptr float, float* %".7", i32 %".6"
  %".9" = load i32, i32* %"i_somaVetores"
  %".10" = getelementptr [1024 x float], [1024 x float]* @"B", i32 0, i32 0
  %".11" = getelementptr float, float* %".10", i32 %".9"
  %".12" = load float, float* %".8"
  %".13" = load float, float* %".11"
  %"tempadd" = fadd float %".12", %".13"
  %".14" = load i32, i32* %"i_somaVetores"
  %".15" = getelementptr [1024 x float], [1024 x float]* @"C", i32 0, i32 0
  %".16" = getelementptr float, float* %".15", i32 %".14"
  store float %"tempadd", float* %".16"
  %".18" = load i32, i32* %"i_somaVetores"
  %"tempadd.1" = add i32 %".18", 1
  store i32 %"tempadd.1", i32* %"i_somaVetores"
  %".20" = load i32, i32* %"i_somaVetores"
  %"tempcmp" = icmp eq i32 %".20", %".1"
  br i1 %"tempcmp", label %"repeat", label %"repeat_end"
repeat_end:
  ret void
}

define i32 @"main"() 
{
main_entry:
  %"i_principal" = alloca i32, align 4
  store i32 0, i32* %"i_principal"
  store i32 0, i32* %"i_principal"
  br label %"repeat"
repeat:
  %".5" = sitofp i32 1 to float
  %".6" = load i32, i32* %"i_principal"
  %".7" = getelementptr [1024 x float], [1024 x float]* @"A", i32 0, i32 0
  %".8" = getelementptr float, float* %".7", i32 %".6"
  store float %".5", float* %".8"
  %".10" = sitofp i32 1 to float
  %".11" = load i32, i32* %"i_principal"
  %".12" = getelementptr [1024 x float], [1024 x float]* @"B", i32 0, i32 0
  %".13" = getelementptr float, float* %".12", i32 %".11"
  store float %".10", float* %".13"
  %".15" = load i32, i32* %"i_principal"
  %"tempadd" = add i32 %".15", 1
  store i32 %"tempadd", i32* %"i_principal"
  %".17" = load i32, i32* %"i_principal"
  %"tempcmp" = icmp eq i32 %".17", 1024
  br i1 %"tempcmp", label %"repeat", label %"repeat_end"
repeat_end:
  call void @"somaVetores"(i32 1024)
  store i32 0, i32* %"i_principal"
  br label %"repeat.1"
repeat.1:
  %".22" = load i32, i32* %"i_principal"
  %".23" = getelementptr [1024 x float], [1024 x float]* @"C", i32 0, i32 0
  %".24" = getelementptr float, float* %".23", i32 %".22"
  %".25" = load float, float* %".24"
  %".26" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".27" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".28" = call i32 (i8*, ...) @"printf"(i8* %".27", float %".25")
  %".29" = load i32, i32* %"i_principal"
  %"tempadd.1" = add i32 %".29", 1
  store i32 %"tempadd.1", i32* %"i_principal"
  %".31" = load i32, i32* %"i_principal"
  %"tempcmp.1" = icmp eq i32 %".31", 1024
  br i1 %"tempcmp.1", label %"repeat.1", label %"repeat_end.1"
repeat_end.1:
  ret i32 0
}
