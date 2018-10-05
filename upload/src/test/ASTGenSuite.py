import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    def test_simple_program300(self):
        input = """ var i:integer;
                    j,k:real;
                procedure main();
                begin
                end
            """
        expect = str(Program([VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),FloatType()),VarDecl(Id(r'k'),FloatType()),FuncDecl(Id("main"),[],[],[],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,300))
    def test_simple_program301(self):
        input = """var i:array [-3 .. -2] of integer;
procedure main();
begin
end
var j,x:array [-1 .. -2] of string;
"""
        expect = "Program([VarDecl(Id(i),ArrayType(-3,-2,IntType)),FuncDecl(Id(main),[],VoidType(),[],[]),VarDecl(Id(j),ArrayType(-1,-2,StringType)),VarDecl(Id(x),ArrayType(-1,-2,StringType))])"
        self.assertTrue(TestAST.test(input,expect,301))
    def test_simple_program302(self):
        input = """procedure main(a:INTEGER;b,c:REAL);
begin
end
"""
        expect = "Program([FuncDecl(Id(main),[VarDecl(Id(a),IntType),VarDecl(Id(b),FloatType),VarDecl(Id(c),FloatType)],VoidType(),[],[])])"
        self.assertTrue(TestAST.test(input,expect,302))
    def test_simple_program303(self):
        input = """procedure main(a:INTEGER;b:real;c:real;d:boolean;e:boolean;f:boolean);
var b:rEAL;c:boolean;d:boolean;e,f,h:array[1 .. 2] of real;
begin
end
"""
        expect = "Program([FuncDecl(Id(main),[VarDecl(Id(a),IntType),VarDecl(Id(b),FloatType),VarDecl(Id(c),FloatType),VarDecl(Id(d),BoolType),VarDecl(Id(e),BoolType),VarDecl(Id(f),BoolType)],VoidType(),[VarDecl(Id(b),FloatType),VarDecl(Id(c),BoolType),VarDecl(Id(d),BoolType),VarDecl(Id(e),ArrayType(1,2,FloatType)),VarDecl(Id(f),ArrayType(1,2,FloatType)),VarDecl(Id(h),ArrayType(1,2,FloatType))],[])])"
        self.assertTrue(TestAST.test(input,expect,303))
    def test_simple_program304(self):
        input = """procedure main(); 
begin 
	with a:real;b,c:boolean;d:INTEGER; do begin
		with a:integer; do begin end
		with b:real;c,d:integer; do begin end
	end
end
"""
        expect = "Program([FuncDecl(Id(main),[],VoidType(),[],[With([VarDecl(Id(a),FloatType),VarDecl(Id(b),BoolType),VarDecl(Id(c),BoolType),VarDecl(Id(d),IntType)],[With([VarDecl(Id(a),IntType)],[]),With([VarDecl(Id(b),FloatType),VarDecl(Id(c),IntType),VarDecl(Id(d),IntType)],[])])])])"
        self.assertTrue(TestAST.test(input,expect,304))
    def test_simple_program305(self):
        input = """procedure main(); 
	begin
	if a > 3 then if a < 6 then a := 1; 
	else a := 3; else a := 6;
	end 
"""
        expect = "Program([FuncDecl(Id(main),[],VoidType(),[],[If(BinaryOp(>,Id(a),IntLiteral(3)),[If(BinaryOp(<,Id(a),IntLiteral(6)),[AssignStmt(Id(a),IntLiteral(1))],[AssignStmt(Id(a),IntLiteral(3))])],[AssignStmt(Id(a),IntLiteral(6))])])])"
        self.assertTrue(TestAST.test(input,expect,305))
    def test_simple_program306(self):
        input = """procedure main(); 
begin
for a := 4 downto 10 do begin end
end
"""
        expect = "Program([FuncDecl(Id(main),[],VoidType(),[],[For(Id(a),IntLiteral(4),IntLiteral(10),False,[])])])"
        self.assertTrue(TestAST.test(input,expect,306))
    def test_simple_program307(self):
        input = """function main():integer;
begin
return 3;
end
"""
        expect = "Program([FuncDecl(Id(main),[],IntType,[],[Return(Some(IntLiteral(3)))])])"
        self.assertTrue(TestAST.test(input,expect,307))
    def test_simple_program308(self):
        input = """procedure main(); 
	begin
	a := a > b or else not c >= d;
	end
"""
        expect = "Program([FuncDecl(Id(main),[],VoidType(),[],[AssignStmt(Id(a),BinaryOp(orelse,BinaryOp(>,Id(a),Id(b)),BinaryOp(>=,UnaryOp(not,Id(c)),Id(d))))])])"
        self.assertTrue(TestAST.test(input,expect,308))
    def test_complex_program309(self):
        input = """function foo(n:integer;x:array[1 .. 10] of integer):array [1 .. 10] of integer;
var b:array[1 .. 10] of integer;
begin
	with i:integer; do 
		if n > 0 then
			for i := n downto a[n] do begin
				b[i] := a[i] + x[i];
				if i = a[x[i]] then
					return x;
				else
					continue;
			end
		else
			for i := 1 to n mod a[n] do begin
				b[i] := a[i] and then x[i] or else b[i];
				if a[x[i]] then
					return x;
				else
					break;
			end
	return foo(foo(x),a[x[n]]);
end
procedure main(); 
var i:integer;
begin
	i := getIntLn();
	foo(a,i);
	with i:integer; do
		for i := 1 to 10 do
			putIntLn(a[i]);
end
var a:array[1 .. 10] of integer;
"""
        expect = "Program([FuncDecl(Id(foo),[VarDecl(Id(n),IntType),VarDecl(Id(x),ArrayType(1,10,IntType))],ArrayType(1,10,IntType),[VarDecl(Id(b),ArrayType(1,10,IntType))],[With([VarDecl(Id(i),IntType)],[If(BinaryOp(>,Id(n),IntLiteral(0)),[For(Id(i),Id(n),ArrayCell(Id(a),Id(n)),False,[AssignStmt(ArrayCell(Id(b),Id(i)),BinaryOp(+,ArrayCell(Id(a),Id(i)),ArrayCell(Id(x),Id(i)))),If(BinaryOp(=,Id(i),ArrayCell(Id(a),ArrayCell(Id(x),Id(i)))),[Return(Some(Id(x)))],[Continue])])],[For(Id(i),IntLiteral(1),BinaryOp(mod,Id(n),ArrayCell(Id(a),Id(n))),True,[AssignStmt(ArrayCell(Id(b),Id(i)),BinaryOp(orelse,BinaryOp(andthen,ArrayCell(Id(a),Id(i)),ArrayCell(Id(x),Id(i))),ArrayCell(Id(b),Id(i)))),If(ArrayCell(Id(a),ArrayCell(Id(x),Id(i))),[Return(Some(Id(x)))],[Break])])])]),Return(Some(CallExpr(Id(foo),[CallExpr(Id(foo),[Id(x)]),ArrayCell(Id(a),ArrayCell(Id(x),Id(n)))])))]),FuncDecl(Id(main),[],VoidType(),[VarDecl(Id(i),IntType)],[AssignStmt(Id(i),CallExpr(Id(getIntLn),[])),CallStmt(Id(foo),[Id(a),Id(i)]),With([VarDecl(Id(i),IntType)],[For(Id(i),IntLiteral(1),IntLiteral(10),True,[CallStmt(Id(putIntLn),[ArrayCell(Id(a),Id(i))])])])]),VarDecl(Id(a),ArrayType(1,10,IntType))])"
        self.assertTrue(TestAST.test(input,expect,309))
    def test_if_program310(self):
        input = """ procedure main();
                begin
                    if a = b then 
                        if a = c then
                            return x;
                    else
                        return y;
                end
"""
        expect = "Program([FuncDecl(Id(main),[],VoidType(),[],[If(BinaryOp(=,Id(a),Id(b)),[If(BinaryOp(=,Id(a),Id(c)),[Return(Some(Id(x)))],[Return(Some(Id(y)))])],[])])])"
        self.assertTrue(TestAST.test(input,expect,310))
    def test_simple_procedure311(self):
        input = """procedure foo (a , b : integer ; c : real) ;
                var x , y : real ;
                begin
                    a := 5;
                end"""
        expect = "Program([FuncDecl(Id(foo),[VarDecl(Id(a),IntType),VarDecl(Id(b),IntType),VarDecl(Id(c),FloatType)],VoidType(),[VarDecl(Id(x),FloatType),VarDecl(Id(y),FloatType)],[AssignStmt(Id(a),IntLiteral(5))])])"
        self.assertTrue(TestAST.test(input,expect,311))
    def test_simple_function312(self):
        input = """function foo (i :integer) : real;var x , y : real; begin //TO DO  end"""
        expect = "Program([FuncDecl(Id(foo),[VarDecl(Id(i),IntType)],FloatType,[VarDecl(Id(x),FloatType),VarDecl(Id(y),FloatType)],[])])"
        self.assertTrue(TestAST.test(input,expect,312))
    def test_var_313(self):
        input = """
            var a, b, c: integer;
            procedure main();
            begin
            a := 1 + 2;
            end
        """
        expect = "Program([VarDecl(Id(a),IntType),VarDecl(Id(b),IntType),VarDecl(Id(c),IntType),FuncDecl(Id(main),[],VoidType(),[],[AssignStmt(Id(a),BinaryOp(+,IntLiteral(1),IntLiteral(2)))])])"
        self.assertTrue(TestAST.test(input,expect,313))
    def test_var_314(self):
        input =  """ var a,b,c: integer;
                           e,f: real;
                        d: array [1 .. 5] of integer;
                """
        expect = "Program([VarDecl(Id(a),IntType),VarDecl(Id(b),IntType),VarDecl(Id(c),IntType),VarDecl(Id(e),FloatType),VarDecl(Id(f),FloatType),VarDecl(Id(d),ArrayType(1,5,IntType))])"
        self.assertTrue(TestAST.test(input,expect,314))
    def test_break_315(self):
        input = """
var
   d: real;
procedure main();
begin
   while  a = true do
   begin   
      if( a > 15) then       
      break;
   end
end
        """
        expect = "Program([VarDecl(Id(d),FloatType),FuncDecl(Id(main),[],VoidType(),[],[While(BinaryOp(=,Id(a),BooleanLiteral(true)),[If(BinaryOp(>,Id(a),IntLiteral(15)),[Break],[])])])])"
        self.assertTrue(TestAST.test(input,expect,315))
    def test_array_dec_316(self):
        input = """
        var  d: array [-4 .. 2] of integer ;          
        """
        expect = str(Program([VarDecl(Id(r'd'),ArrayType(-4,2,IntType()))]))
        self.assertTrue(TestAST.test(input,expect,316))
    def test_assign_317(self):
        input = """procedurE inndeeexxx();
        begin
            (e>d)[5] := abc+a[1][2]; 
            foo(2)[a+3] := 5;
            ca[1][10] := 123;
        end"""
        expect = str(Program([FuncDecl(Id(r'inndeeexxx'),[],[],[Assign(ArrayCell(BinaryOp(r'>',Id(r'e'),Id(r'd')),IntLiteral(5)),BinaryOp(r'+',Id(r'abc'),ArrayCell(ArrayCell(Id(r'a'),IntLiteral(1)),IntLiteral(2)))),Assign(ArrayCell(CallExpr(Id(r'foo'),[IntLiteral(2)]),BinaryOp(r'+',Id(r'a'),IntLiteral(3))),IntLiteral(5)),Assign(ArrayCell(ArrayCell(Id(r'ca'),IntLiteral(1)),IntLiteral(10)),IntLiteral(123))],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,317))      
    def test_arrayelement_318(self):
        input = """procedure foo(a : integer;b : real);
    begin
        e := (3+4)/3;
        putint(a);
        a := b[4];
    return;
    end
        """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),FloatType())],[],[Assign(Id(r'e'),BinaryOp(r'/',BinaryOp(r'+',IntLiteral(3),IntLiteral(4)),IntLiteral(3))),CallStmt(Id(r'putint'),[Id(r'a')]),Assign(Id(r'a'),ArrayCell(Id(r'b'),IntLiteral(4))),Return(None)],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,318))
    def test_multiassign_319(self):
        input = """
                procedure calculator();
var
a,b,c : integer;
d: real;

begin
   a:=21;
   b:=10;
   c := a + b;
   c := a - b;

   c := a * b;
   
   d := a / b;
   
   c := a mod b;
   
   c := a div b;
   
      writeln("Line 6 - Value of c is ", c );
end

            """
        expect = str(Program([FuncDecl(Id(r'calculator'),[],[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'd'),FloatType())],[Assign(Id(r'a'),IntLiteral(21)),Assign(Id(r'b'),IntLiteral(10)),Assign(Id(r'c'),BinaryOp(r'+',Id(r'a'),Id(r'b'))),Assign(Id(r'c'),BinaryOp(r'-',Id(r'a'),Id(r'b'))),Assign(Id(r'c'),BinaryOp(r'*',Id(r'a'),Id(r'b'))),Assign(Id(r'd'),BinaryOp(r'/',Id(r'a'),Id(r'b'))),Assign(Id(r'c'),BinaryOp(r'mod',Id(r'a'),Id(r'b'))),Assign(Id(r'c'),BinaryOp(r'div',Id(r'a'),Id(r'b'))),CallStmt(Id(r'writeln'),[StringLiteral(r'Line 6 - Value of c is '),Id(r'c')])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,319))
    
    def test_string325(self):
        input = """
Var
	S : String;

Procedure main();
Begin
	S := "Hey there! How are you?";
	Write("The word \\"How\\" is found at char index ");
	Writeln(Pos("How", S));
	If Pos("Why", S) <= 0 Then
		Writeln("\\"Why\\" is not found.");
End
        """
        expect = str(Program([VarDecl(Id(r'S'),StringType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'S'),StringLiteral(r'Hey there! How are you?')),CallStmt(Id(r'Write'),[StringLiteral(r'The word \"How\" is found at char index ')]),CallStmt(Id(r'Writeln'),[CallExpr(Id(r'Pos'),[StringLiteral(r'How'),Id(r'S')])]),If(BinaryOp(r'<=',CallExpr(Id(r'Pos'),[StringLiteral(r'Why'),Id(r'S')]),IntLiteral(0)),[CallStmt(Id(r'Writeln'),[StringLiteral(r'\"Why\" is not found.')])],[])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,325))
    def test_or_330(self):
        input = """
Var n1, n2 : string;
procedure main();
Begin
    Writeln("Enter two numbers to exit");
    While not ((n1 = "0") OR (n2 = "0")) do
    Begin
        write(n1);
        write(n2);
    End
End
        """
        expect = str(Program([VarDecl(Id(r'n1'),StringType()),VarDecl(Id(r'n2'),StringType()),FuncDecl(Id(r'main'),[],[],[CallStmt(Id(r'Writeln'),[StringLiteral(r'Enter two numbers to exit')]),While(UnaryOp(r'not',BinaryOp(r'OR',BinaryOp(r'=',Id(r'n1'),StringLiteral(r'0')),BinaryOp(r'=',Id(r'n2'),StringLiteral(r'0')))),[CallStmt(Id(r'write'),[Id(r'n1')]),CallStmt(Id(r'write'),[Id(r'n2')])])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,330))

    def test_complex_350(self):
        input = """
                procedure qsort_recur();
                BEGIN { QuicksortRecur }
                { If there's anything to do... }
                IF start < stop THEN 
                    BEGIN
                        splitpt := Split(start, stop);
                        QuicksortRecur(start, splitpt-1);
                        QuicksortRecur(splitpt+1, stop);
                    END
                END
                """
        expect = str(Program([FuncDecl(Id(r'qsort_recur'),[],[],[If(BinaryOp(r'<',Id(r'start'),Id(r'stop')),[Assign(Id(r'splitpt'),CallExpr(Id(r'Split'),[Id(r'start'),Id(r'stop')])),CallStmt(Id(r'QuicksortRecur'),[Id(r'start'),BinaryOp(r'-',Id(r'splitpt'),IntLiteral(1))]),CallStmt(Id(r'QuicksortRecur'),[BinaryOp(r'+',Id(r'splitpt'),IntLiteral(1)),Id(r'stop')])],[])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,350))
    def test_factorial_370(self):
        input = """
Function Factorial(n : Integer) : Integer;
Var
	Result : Integer;
	i : Integer;

Begin
	Result := n;
	If (n <= 1) Then
		Result := 1;
	Else
	For i := n-1 DownTo 1 do
		Result := Result * i; 
	Factorial := Result;
End
        """
        expect = str(Program([FuncDecl(Id(r'Factorial'),[VarDecl(Id(r'n'),IntType())],[VarDecl(Id(r'Result'),IntType()),VarDecl(Id(r'i'),IntType())],[Assign(Id(r'Result'),Id(r'n')),If(BinaryOp(r'<=',Id(r'n'),IntLiteral(1)),[Assign(Id(r'Result'),IntLiteral(1))],[For(Id(r'i'),BinaryOp(r'-',Id(r'n'),IntLiteral(1)),IntLiteral(1),False,[Assign(Id(r'Result'),BinaryOp(r'*',Id(r'Result'),Id(r'i')))])]),Assign(Id(r'Factorial'),Id(r'Result'))],IntType())]))
        self.assertTrue(TestAST.test(input,expect,370))
    def test_fibonancy_371(self):
        input = """
var
   i: integer;
function fibonacci(n: integer): integer;

begin
   if n=1 then
      fibonacci := 0;
   
   else if n=2 then
      fibonacci := 1;
   
   else
      fibonacci := fibonacci(n-1) + fibonacci(n-2);
end

procedure main();
begin
   for i:= 1 to 10 do
   
   write(fibonacci (i), "  ");
end
        """
        expect = str(Program([VarDecl(Id(r'i'),IntType()),FuncDecl(Id(r'fibonacci'),[VarDecl(Id(r'n'),IntType())],[],[If(BinaryOp(r'=',Id(r'n'),IntLiteral(1)),[Assign(Id(r'fibonacci'),IntLiteral(0))],[If(BinaryOp(r'=',Id(r'n'),IntLiteral(2)),[Assign(Id(r'fibonacci'),IntLiteral(1))],[Assign(Id(r'fibonacci'),BinaryOp(r'+',CallExpr(Id(r'fibonacci'),[BinaryOp(r'-',Id(r'n'),IntLiteral(1))]),CallExpr(Id(r'fibonacci'),[BinaryOp(r'-',Id(r'n'),IntLiteral(2))])))])])],IntType()),FuncDecl(Id(r'main'),[],[],[For(Id(r'i'),IntLiteral(1),IntLiteral(10),True,[CallStmt(Id(r'write'),[CallExpr(Id(r'fibonacci'),[Id(r'i')]),StringLiteral(r'  ')])])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,371))
