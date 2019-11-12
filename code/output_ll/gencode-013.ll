; ModuleID = "gencode-013.ll"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"__isoc99_scanf"(i8* %".1", ...) 

declare i32 @"printf"(i8* %".1", ...) 

@"fstr_int_scan" = internal global [3 x i8] c"%i\00", align 4
@"fstr_float_scan" = internal global [3 x i8] c"%f\00", align 4
@"fstr_int" = internal global [4 x i8] c"%i\0a\00", align 4
@"fstr_float" = internal global [4 x i8] c"%f\0a\00", align 4
define i32 @"maiorde2"(i32 %".1", i32 %".2") 
{
maiorde2_entry:
  %".4" = alloca i32, align 4
  store i32 %".1", i32* %".4"
  %".6" = alloca i32, align 4
  store i32 %".2", i32* %".6"
  %".8" = load i32, i32* %".4"
  %".9" = load i32, i32* %".6"
  %"tempcmp" = icmp sgt i32 %".8", %".9"
  br i1 %"tempcmp", label %"maiorde2_entry.if", label %"maiorde2_entry.endif"
maiorde2_entry.if:
  %".11" = load i32, i32* %".4"
  ret i32 %".11"
maiorde2_entry.endif:
  %".13" = load i32, i32* %".6"
  ret i32 %".13"
}

define i32 @"maiorde4"(i32 %".1", i32 %".2", i32 %".3", i32 %".4") 
{
maiorde4_entry:
  %".6" = alloca i32, align 4
  store i32 %".1", i32* %".6"
  %".8" = alloca i32, align 4
  store i32 %".2", i32* %".8"
  %".10" = alloca i32, align 4
  store i32 %".3", i32* %".10"
  %".12" = alloca i32, align 4
  store i32 %".4", i32* %".12"
  %".14" = load i32, i32* %".6"
  %".15" = load i32, i32* %".8"
  %".16" = call i32 @"maiorde2"(i32 %".14", i32 %".15")
  %".17" = load i32, i32* %".10"
  %".18" = load i32, i32* %".12"
  %".19" = call i32 @"maiorde2"(i32 %".17", i32 %".18")
  %".20" = call i32 @"maiorde2"(i32 %".16", i32 %".19")
  ret i32 %".20"
}

define i32 @"main"() 
{
main_entry:
  %"A_principal" = alloca i32, align 4
  store i32 0, i32* %"A_principal"
  %"B_principal" = alloca i32, align 4
  store i32 0, i32* %"B_principal"
  %"C_principal" = alloca i32, align 4
  store i32 0, i32* %"C_principal"
  %"D_principal" = alloca i32, align 4
  store i32 0, i32* %"D_principal"
  %".6" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".7" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".8" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".6", i32* %"A_principal")
  %".9" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".10" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".11" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".9", i32* %"B_principal")
  %".12" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".13" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".14" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".12", i32* %"C_principal")
  %".15" = bitcast [3 x i8]* @"fstr_int_scan" to i8*
  %".16" = bitcast [3 x i8]* @"fstr_float_scan" to i8*
  %".17" = call i32 (i8*, ...) @"__isoc99_scanf"(i8* %".15", i32* %"D_principal")
  %".18" = load i32, i32* %"A_principal"
  %".19" = load i32, i32* %"B_principal"
  %".20" = load i32, i32* %"C_principal"
  %".21" = load i32, i32* %"D_principal"
  %".22" = call i32 @"maiorde4"(i32 %".18", i32 %".19", i32 %".20", i32 %".21")
  %".23" = bitcast [4 x i8]* @"fstr_int" to i8*
  %".24" = bitcast [4 x i8]* @"fstr_float" to i8*
  %".25" = call i32 (i8*, ...) @"printf"(i8* %".23", i32 %".22")
  ret i32 0
}
