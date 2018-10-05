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
        expect = str(Program([VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),FloatType()),VarDecl(Id(r'k'),FloatType()),FuncDecl(Id(r'main'),[],[],[],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,300))
    def test_simple_program301(self):
        input = """var i:array [-3 .. -2] of integer;
procedure main();
begin
end
var j,x:array [-1 .. -2] of string;
"""
        expect = str(Program([VarDecl(Id(r'i'),ArrayType(-3,-2,IntType())),FuncDecl(Id(r'main'),[],[],[],VoidType()),VarDecl(Id(r'j'),ArrayType(-1,-2,StringType())),VarDecl(Id(r'x'),ArrayType(-1,-2,StringType()))]))
        self.assertTrue(TestAST.test(input,expect,301))
    def test_simple_program302(self):
        input = """procedure main(a:INTEGER;b,c:REAL);
begin
end
"""
        expect = str(Program([FuncDecl(Id(r'main'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),FloatType()),VarDecl(Id(r'c'),FloatType())],[],[],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,302))
    def test_simple_program303(self):
        input = """procedure main(a:INTEGER;b:real;c:real;d:boolean;e:boolean;f:boolean);
var b:rEAL;c:boolean;d:boolean;e,f,h:array[1 .. 2] of real;
begin
end
"""
        expect = str(Program([FuncDecl(Id(r'main'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),FloatType()),VarDecl(Id(r'c'),FloatType()),VarDecl(Id(r'd'),BoolType()),VarDecl(Id(r'e'),BoolType()),VarDecl(Id(r'f'),BoolType())],[VarDecl(Id(r'b'),FloatType()),VarDecl(Id(r'c'),BoolType()),VarDecl(Id(r'd'),BoolType()),VarDecl(Id(r'e'),ArrayType(1,2,FloatType())),VarDecl(Id(r'f'),ArrayType(1,2,FloatType())),VarDecl(Id(r'h'),ArrayType(1,2,FloatType()))],[],VoidType())]))
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
        expect = str(Program([FuncDecl(Id(r'main'),[],[],[With([VarDecl(Id(r'a'),FloatType()),VarDecl(Id(r'b'),BoolType()),VarDecl(Id(r'c'),BoolType()),VarDecl(Id(r'd'),IntType())],[With([VarDecl(Id(r'a'),IntType())],[]),With([VarDecl(Id(r'b'),FloatType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'd'),IntType())],[])])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,304))
    def test_simple_program305(self):
        input = """procedure main(); 
	begin
	if a > 3 then if a < 6 then a := 1; 
	else a := 3; else a := 6;
	end 
"""
        expect = str(Program([FuncDecl(Id(r'main'),[],[],[If(BinaryOp(r'>',Id(r'a'),IntLiteral(3)),[If(BinaryOp(r'<',Id(r'a'),IntLiteral(6)),[Assign(Id(r'a'),IntLiteral(1))],[Assign(Id(r'a'),IntLiteral(3))])],[Assign(Id(r'a'),IntLiteral(6))])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,305))
    def test_simple_program306(self):
        input = """procedure main(); 
begin
for a := 4 downto 10 do begin end
end
"""
        expect = str(Program([FuncDecl(Id(r'main'),[],[],[For(Id(r'a'),IntLiteral(4),IntLiteral(10),False,[])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,306))
    def test_simple_program307(self):
        input = """function main():integer;
begin
return 3;
end
"""
        expect = str(Program([FuncDecl(Id(r'main'),[],[],[Return(IntLiteral(3))],IntType())]))
        self.assertTrue(TestAST.test(input,expect,307))
    def test_simple_program308(self):
        input = """procedure main(); 
	begin
	a := a > b or else not c >= d;
	end
"""
        expect = str(Program([FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),BinaryOp(r'orelse',BinaryOp(r'>',Id(r'a'),Id(r'b')),BinaryOp(r'>=',UnaryOp(r'not',Id(r'c')),Id(r'd'))))],VoidType())]))
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
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'n'),IntType()),VarDecl(Id(r'x'),ArrayType(1,10,IntType()))],[VarDecl(Id(r'b'),ArrayType(1,10,IntType()))],[With([VarDecl(Id(r'i'),IntType())],[If(BinaryOp(r'>',Id(r'n'),IntLiteral(0)),[For(Id(r'i'),Id(r'n'),ArrayCell(Id(r'a'),Id(r'n')),False,[Assign(ArrayCell(Id(r'b'),Id(r'i')),BinaryOp(r'+',ArrayCell(Id(r'a'),Id(r'i')),ArrayCell(Id(r'x'),Id(r'i')))),If(BinaryOp(r'=',Id(r'i'),ArrayCell(Id(r'a'),ArrayCell(Id(r'x'),Id(r'i')))),[Return(Id(r'x'))],[Continue()])])],[For(Id(r'i'),IntLiteral(1),BinaryOp(r'mod',Id(r'n'),ArrayCell(Id(r'a'),Id(r'n'))),True,[Assign(ArrayCell(Id(r'b'),Id(r'i')),BinaryOp(r'orelse',BinaryOp(r'andthen',ArrayCell(Id(r'a'),Id(r'i')),ArrayCell(Id(r'x'),Id(r'i'))),ArrayCell(Id(r'b'),Id(r'i')))),If(ArrayCell(Id(r'a'),ArrayCell(Id(r'x'),Id(r'i'))),[Return(Id(r'x'))],[Break()])])])]),Return(CallExpr(Id(r'foo'),[CallExpr(Id(r'foo'),[Id(r'x')]),ArrayCell(Id(r'a'),ArrayCell(Id(r'x'),Id(r'n')))]))],ArrayType(1,10,IntType())),FuncDecl(Id(r'main'),[],[VarDecl(Id(r'i'),IntType())],[Assign(Id(r'i'),CallExpr(Id(r'getIntLn'),[])),CallStmt(Id(r'foo'),[Id(r'a'),Id(r'i')]),With([VarDecl(Id(r'i'),IntType())],[For(Id(r'i'),IntLiteral(1),IntLiteral(10),True,[CallStmt(Id(r'putIntLn'),[ArrayCell(Id(r'a'),Id(r'i'))])])])],VoidType()),VarDecl(Id(r'a'),ArrayType(1,10,IntType()))]))
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
        expect = str(Program([FuncDecl(Id(r'main'),[],[],[If(BinaryOp(r'=',Id(r'a'),Id(r'b')),[If(BinaryOp(r'=',Id(r'a'),Id(r'c')),[Return(Id(r'x'))],[Return(Id(r'y'))])],[])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,310))
    def test_simple_procedure311(self):
        input = """procedure foo (a , b : integer ; c : real) ;
                var x , y : real ;
                begin
                    a := 5;
                end"""
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),FloatType())],[VarDecl(Id(r'x'),FloatType()),VarDecl(Id(r'y'),FloatType())],[Assign(Id(r'a'),IntLiteral(5))],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,311))
    def test_simple_function312(self):
        input = """function foo (i :integer) : real;var x , y : real; begin //TO DO  end"""
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'i'),IntType())],[VarDecl(Id(r'x'),FloatType()),VarDecl(Id(r'y'),FloatType())],[],FloatType())]))
        self.assertTrue(TestAST.test(input,expect,312))
    def test_var_313(self):
        input = """
            var a, b, c: integer;
            procedure main();
            begin
            a := 1 + 2;
            end
        """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),BinaryOp(r'+',IntLiteral(1),IntLiteral(2)))],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,313))
    def test_var_314(self):
        input =  """ var a,b,c: integer;
                           e,f: real;
                        d: array [1 .. 5] of integer;
                """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'e'),FloatType()),VarDecl(Id(r'f'),FloatType()),VarDecl(Id(r'd'),ArrayType(1,5,IntType()))]))
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
        expect = str(Program([VarDecl(Id(r'd'),FloatType()),FuncDecl(Id(r'main'),[],[],[While(BinaryOp(r'=',Id(r'a'),BooleanLiteral(True)),[If(BinaryOp(r'>',Id(r'a'),IntLiteral(15)),[Break()],[])])],VoidType())]))
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
    def test_simple_if_320(self):
        input =  """ 
        var a,b: integer;
        procedure main();
            Begin
                a := 1;
                b := 1;
                if(a = b)
                then a:= a - b;
                else b:= b - a;
            END
        """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),IntLiteral(1)),Assign(Id(r'b'),IntLiteral(1)),If(BinaryOp(r'=',Id(r'a'),Id(r'b')),[Assign(Id(r'a'),BinaryOp(r'-',Id(r'a'),Id(r'b')))],[Assign(Id(r'b'),BinaryOp(r'-',Id(r'b'),Id(r'a')))])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,320))
    def test_simple_while_321(self):
        input =  """ 
        var i: integer;
        procedure main();
            Begin
                while i>0
                do
                    i:= i - 1; 
            END
        """
        expect = str(Program([VarDecl(Id(r'i'),IntType()),FuncDecl(Id(r'main'),[],[],[While(BinaryOp(r'>',Id(r'i'),IntLiteral(0)),[Assign(Id(r'i'),BinaryOp(r'-',Id(r'i'),IntLiteral(1)))])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,321))

    def test_simple_for_322(self):
        input =  """ 
        var i: integer;
        procedure main();
            Begin
                for i:=5 downto 1 do
                    i:= i - 1; 
            END
        """
        expect = str(Program([VarDecl(Id(r'i'),IntType()),FuncDecl(Id(r'main'),[],[],[For(Id(r'i'),IntLiteral(5),IntLiteral(1),False,[Assign(Id(r'i'),BinaryOp(r'-',Id(r'i'),IntLiteral(1)))])],VoidType())])) 
        self.assertTrue(TestAST.test(input,expect,322))  

    def test_simple_continue_323(self): 
        input =  """     
        var i: integer;
        procedure main();
            Begin
                for i:=5 downto 1 do
                    i:= i - 1; 
                continue;
            END
        """
        expect = str(Program([VarDecl(Id(r'i'),IntType()),FuncDecl(Id(r'main'),[],[],[For(Id(r'i'),IntLiteral(5),IntLiteral(1),False,[Assign(Id(r'i'),BinaryOp(r'-',Id(r'i'),IntLiteral(1)))]),Continue()],VoidType())])) 
        self.assertTrue(TestAST.test(input,expect,323))

    def test_simple_return_324(self): 
        input =  """ 
                function foo (i :integer) : real;                   
                    Begin
                        a:=b:=c:= 1;
                        e:=f:=1.02;
                        d[1]:=1;
                        return e;
                    End """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'i'),IntType())],[],[Assign(Id(r'a'),IntLiteral(1)),Assign(Id(r'b'),IntLiteral(1)),Assign(Id(r'c'),IntLiteral(1)),Assign(Id(r'e'),FloatLiteral(1.02)),Assign(Id(r'f'),FloatLiteral(1.02)),Assign(ArrayCell(Id(r'd'),IntLiteral(1)),IntLiteral(1)),Return(Id(r'e'))],FloatType())])) 
        self.assertTrue(TestAST.test(input,expect,324))  
    def test_simple_with_325(self): 
        input =  """     
        var i: integer;
        procedure main();
            Begin
                with  i,a: integer; do
                    i:= i - 1; 
            END
        """
        expect = str(Program([VarDecl(Id(r'i'),IntType()),FuncDecl(Id(r'main'),[],[],[With([VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'a'),IntType())],[Assign(Id(r'i'),BinaryOp(r'-',Id(r'i'),IntLiteral(1)))])],VoidType())])) 
        self.assertTrue(TestAST.test(input,expect,325))  
    def test_simple_program_326(self):
        input = """        
        var i,n,f1,f2: integer;
        function fibo(n: integer): integer;
        begin
            f1:=0;
            f2:=1;
            for i:=1 to n do
            begin
            f2:=f2+f1;
            f1:=f2-f1;
            end
        end"""
        expect = str(Program([VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'n'),IntType()),VarDecl(Id(r'f1'),IntType()),VarDecl(Id(r'f2'),IntType()),FuncDecl(Id(r'fibo'),[VarDecl(Id(r'n'),IntType())],[],[Assign(Id(r'f1'),IntLiteral(0)),Assign(Id(r'f2'),IntLiteral(1)),For(Id(r'i'),IntLiteral(1),Id(r'n'),True,[Assign(Id(r'f2'),BinaryOp(r'+',Id(r'f2'),Id(r'f1'))),Assign(Id(r'f1'),BinaryOp(r'-',Id(r'f2'),Id(r'f1')))])],IntType())]))

        self.assertTrue(TestAST.test(input,expect,326))
    def test_complex_if_327(self):
        input = """  
        var a,b,c,d: integer;
        function danhgia(diem: integer): integer;
        begin
            if(diem > d) then writeln("gioi");
            else if(diem > c) then writeln("kha");
            else if(diem > b) then writeln("TB");
            else if(diem > a) then writeln("yeu");
            else writeln("kem");
        end"""
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'd'),IntType()),FuncDecl(Id(r'danhgia'),[VarDecl(Id(r'diem'),IntType())],[],[If(BinaryOp(r'>',Id(r'diem'),Id(r'd')),[CallStmt(Id(r'writeln'),[StringLiteral(r'gioi')])],[If(BinaryOp(r'>',Id(r'diem'),Id(r'c')),[CallStmt(Id(r'writeln'),[StringLiteral(r'kha')])],[If(BinaryOp(r'>',Id(r'diem'),Id(r'b')),[CallStmt(Id(r'writeln'),[StringLiteral(r'TB')])],[If(BinaryOp(r'>',Id(r'diem'),Id(r'a')),[CallStmt(Id(r'writeln'),[StringLiteral(r'yeu')])],[CallStmt(Id(r'writeln'),[StringLiteral(r'kem')])])])])])],IntType())]))
        self.assertTrue(TestAST.test(input,expect,327))
    def test_complex_while_328(self):
        input = """  
        var a,b,c,d: integer;
        function foo(): integer;
        begin
            while(true) do
                while (a = b and c + d) do a:= b; break;
        end     """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'd'),IntType()),FuncDecl(Id(r'foo'),[],[],[While(BooleanLiteral(True),[While(BinaryOp(r'=',Id(r'a'),BinaryOp(r'+',BinaryOp(r'and',Id(r'b'),Id(r'c')),Id(r'd'))),[Assign(Id(r'a'),Id(r'b'))])]),Break()],IntType())]))
        self.assertTrue(TestAST.test(input,expect,328))

    def test_simple_break_329(self): 
        input =  """     
        var i: integer;
        procedure main();
            Begin
                for i:=5 downto 1 do
                    i:= i - 1; 
                break;
            END
        """
        expect = str(Program([VarDecl(Id(r'i'),IntType()),FuncDecl(Id(r'main'),[],[],[For(Id(r'i'),IntLiteral(5),IntLiteral(1),False,[Assign(Id(r'i'),BinaryOp(r'-',Id(r'i'),IntLiteral(1)))]),Break()],VoidType())])) 
        self.assertTrue(TestAST.test(input,expect,329))

    def test_and_330(self):
        input = """
Var age : Integer;
procedure main();
Begin
	While (age > 0) AND (age <= 100) Do
    Begin
		Write("Enter age (1 - 100): ");
		Readln(age);
		If (age < 1) Then
			Writeln("Age cannot be less than 1...");
		Else If (age > 100) Then
			Writeln("Age cannot be greater than 100...");
    End
End
        """
        expect = str(Program([VarDecl(Id(r'age'),IntType()),FuncDecl(Id(r'main'),[],[],[While(BinaryOp(r'AND',BinaryOp(r'>',Id(r'age'),IntLiteral(0)),BinaryOp(r'<=',Id(r'age'),IntLiteral(100))),[CallStmt(Id(r'Write'),[StringLiteral(r'Enter age (1 - 100): ')]),CallStmt(Id(r'Readln'),[Id(r'age')]),If(BinaryOp(r'<',Id(r'age'),IntLiteral(1)),[CallStmt(Id(r'Writeln'),[StringLiteral(r'Age cannot be less than 1...')])],[If(BinaryOp(r'>',Id(r'age'),IntLiteral(100)),[CallStmt(Id(r'Writeln'),[StringLiteral(r'Age cannot be greater than 100...')])],[])])])],VoidType())])) 
        self.assertTrue(TestAST.test(input,expect,330))

    def test_bool_331(self):
        input = """
Var 
	bool : Boolean;
	A, B : Integer;
Procedure main();
Begin
	A := 10;
	B := 30;
	bool := FAlse;
	bool := (A = 10) OR (B = 10);
	Writeln(bool); 
	bool := (A = 10) AND (B = 10);
	Writeln(bool); 
End
        """
        expect = str(Program([VarDecl(Id(r'bool'),BoolType()),VarDecl(Id(r'A'),IntType()),VarDecl(Id(r'B'),IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'A'),IntLiteral(10)),Assign(Id(r'B'),IntLiteral(30)),Assign(Id(r'bool'),BooleanLiteral(False)),Assign(Id(r'bool'),BinaryOp(r'OR',BinaryOp(r'=',Id(r'A'),IntLiteral(10)),BinaryOp(r'=',Id(r'B'),IntLiteral(10)))),CallStmt(Id(r'Writeln'),[Id(r'bool')]),Assign(Id(r'bool'),BinaryOp(r'AND',BinaryOp(r'=',Id(r'A'),IntLiteral(10)),BinaryOp(r'=',Id(r'B'),IntLiteral(10)))),CallStmt(Id(r'Writeln'),[Id(r'bool')])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,331))
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
