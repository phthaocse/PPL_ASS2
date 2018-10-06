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
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'i'),IntType())],[],[Assign(Id(r'c'),IntLiteral(1)),Assign(Id(r'b'),Id(r'c')),Assign(Id(r'a'),Id(r'b')),Assign(Id(r'f'),FloatLiteral(1.02)),Assign(Id(r'e'),Id(r'f')),Assign(ArrayCell(Id(r'd'),IntLiteral(1)),IntLiteral(1)),Return(Id(r'e'))],FloatType())])) 
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
    def test_assign_332(self):
        input = """        var a,b,c: integer;
        procedure main();
        Begin
            a := b := c := 1;
            a[1] := b[1] := c[1];
        End"""
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'c'),IntLiteral(1)),Assign(Id(r'b'),Id(r'c')),Assign(Id(r'a'),Id(r'b')),Assign(ArrayCell(Id(r'b'),IntLiteral(1)),ArrayCell(Id(r'c'),IntLiteral(1))),Assign(ArrayCell(Id(r'a'),IntLiteral(1)),ArrayCell(Id(r'b'),IntLiteral(1)))],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,332))

    def test_callstmt_333(self):
        input = """        
        procedure main();
        Begin
            foo(x);
            fibonancy(a1,a2);
            fac(5);
            sum(a[1],b[1],d[5]);
            div(a*5,b*8);
        End"""
        expect = str(Program([FuncDecl(Id(r'main'),[],[],[CallStmt(Id(r'foo'),[Id(r'x')]),CallStmt(Id(r'fibonancy'),[Id(r'a1'),Id(r'a2')]),CallStmt(Id(r'fac'),[IntLiteral(5)]),CallStmt(Id(r'sum'),[ArrayCell(Id(r'a'),IntLiteral(1)),ArrayCell(Id(r'b'),IntLiteral(1)),ArrayCell(Id(r'd'),IntLiteral(5))])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,333))
    def test_procedure_334(self):
        input = """procedure test(n:integer;x:array[1 .. 10] of integer; b:real; c:boolean);var arr:array[1 .. 10] of integer;
        Begin
            if (a = 1) then 
                a := 2;
            else 
                a := 0;
        End"""
        expect = str(Program([FuncDecl(Id(r'test'),[VarDecl(Id(r'n'),IntType()),VarDecl(Id(r'x'),ArrayType(1,10,IntType())),VarDecl(Id(r'b'),FloatType()),VarDecl(Id(r'c'),BoolType())],[VarDecl(Id(r'arr'),ArrayType(1,10,IntType()))],[If(BinaryOp(r'=',Id(r'a'),IntLiteral(1)),[Assign(Id(r'a'),IntLiteral(2))],[Assign(Id(r'a'),IntLiteral(0))])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,334))
    def test_fundec_335(self):
        input = """function foo(a:array[1 .. 5] of integer;b:array[1 .. 5] of integer;d:array[1 .. 5] of integer):array [1 .. 5] of integer;
var arr:array[1 .. 5] of integer;
        begin
            foo();
            fibonancy(a1,a2);
            fac(5);
            sum(a[1],b[1],d[5]);
            div(a*5,b*8);
          return arr;
        end"""
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),ArrayType(1,5,IntType())),VarDecl(Id(r'b'),ArrayType(1,5,IntType())),VarDecl(Id(r'd'),ArrayType(1,5,IntType()))],[VarDecl(Id(r'arr'),ArrayType(1,5,IntType()))],[CallStmt(Id(r'foo'),[]),CallStmt(Id(r'fibonancy'),[Id(r'a1'),Id(r'a2')]),CallStmt(Id(r'fac'),[IntLiteral(5)]),CallStmt(Id(r'sum'),[ArrayCell(Id(r'a'),IntLiteral(1)),ArrayCell(Id(r'b'),IntLiteral(1)),ArrayCell(Id(r'd'),IntLiteral(5))])],ArrayType(1,5,IntType()))])) 
        self.assertTrue(TestAST.test(input,expect,335))

    def test_fundec_336(self):
        input = """function foo(n:integer;x:array[1 .. 5] of integer;b:boolean;r:real):array [1 .. 5] of integer;
var arr:array[1 .. 5] of integer;
begin
    return arr;
end"""
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'n'),IntType()),VarDecl(Id(r'x'),ArrayType(1,5,IntType())),VarDecl(Id(r'b'),BoolType()),VarDecl(Id(r'r'),FloatType())],[VarDecl(Id(r'arr'),ArrayType(1,5,IntType()))],[Return(Id(r'arr'))],ArrayType(1,5,IntType()))])) 
        self.assertTrue(TestAST.test(input,expect,336))
    def test_nested_337(self):
        input = """
            procedure main();
            begin
                while(true) do
                begin
                    if(true) then writeln("OK");  
                    else 
                        for i:=1 to 5 do
                            writeln("OK");  
                end
            end"""
        expect = str(Program([FuncDecl(Id(r'main'),[],[],[While(BooleanLiteral(True),[If(BooleanLiteral(True),[CallStmt(Id(r'writeln'),[StringLiteral(r'OK')])],[For(Id(r'i'),IntLiteral(1),IntLiteral(5),True,[CallStmt(Id(r'writeln'),[StringLiteral(r'OK')])])])])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,337))
    def test_string_338(self):
        input = """
        Var
            myString : String;
        Procedure Main();
        Begin
            myString := "qua met";
            
            Write(myString[byte(myString[0])]);

        End"""
        expect = str(Program([VarDecl(Id(r'myString'),StringType()),FuncDecl(Id(r'Main'),[],[],[Assign(Id(r'myString'),StringLiteral(r'qua met')),CallStmt(Id(r'Write'),[ArrayCell(Id(r'myString'),CallExpr(Id(r'byte'),[ArrayCell(Id(r'myString'),IntLiteral(0))]))])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,338))
    def test_string_339(self):
        input = """
Var
    myString : String;

Procedure Main();
Begin
	myString := "Hey! How are you?";
	Writeln("The length of the string is ", byte(myString[0]));
	Write(myString[byte(myString[0])]);
	Write(" is the last character.");
End"""
        expect = str(Program([VarDecl(Id(r'myString'),StringType()),FuncDecl(Id(r'Main'),[],[],[Assign(Id(r'myString'),StringLiteral(r'Hey! How are you?')),CallStmt(Id(r'Writeln'),[StringLiteral(r'The length of the string is '),CallExpr(Id(r'byte'),[ArrayCell(Id(r'myString'),IntLiteral(0))])]),CallStmt(Id(r'Write'),[ArrayCell(Id(r'myString'),CallExpr(Id(r'byte'),[ArrayCell(Id(r'myString'),IntLiteral(0))]))]),CallStmt(Id(r'Write'),[StringLiteral(r' is the last character.')])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,339))
    def test_simple_program340(self):
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
        self.assertTrue(TestAST.test(input,expect,340))
    def test_simple_assign_341(self):
        input = """var a: integer;
        procedure main();
            Begin
                a := 1;
            End"""
        expect = str(Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),IntLiteral(1))],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,341))
    def test_complex_assign_342(self):
        input = """
        var a: integer;
        procedure main();
            Begin
                a := b [10] := foo ( ) [3] := x := 1;
            End
        """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'x'),IntLiteral(1)),Assign(ArrayCell(CallExpr(Id(r'foo'),[]),IntLiteral(3)),Id(r'x')),Assign(ArrayCell(Id(r'b'),IntLiteral(10)),ArrayCell(CallExpr(Id(r'foo'),[]),IntLiteral(3))),Assign(Id(r'a'),ArrayCell(Id(r'b'),IntLiteral(10)))],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,342))
    def test_simple_program_343(self):

        input = """function foo (i :integer) : real; begin a:= 5; end
                   var a, b, c: integer;
                   //do something
                   procedure xinchao();
                   bEgin
                     writeln("xin chao");
                   End"""

    
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'i'),IntType())],[],[Assign(Id(r'a'),IntLiteral(5))],FloatType()),VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),FuncDecl(Id(r'xinchao'),[],[],[CallStmt(Id(r'writeln'),[StringLiteral(r'xin chao')])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,343))

    def test_complex_assign_344(self):
        input = """
        var a: integer;
        procedure main();
            Begin
                a := b[10] := foo()[3] := x = 1;
            End
        """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'main'),[],[],[Assign(ArrayCell(CallExpr(Id(r'foo'),[]),IntLiteral(3)),BinaryOp(r'=',Id(r'x'),IntLiteral(1))),Assign(ArrayCell(Id(r'b'),IntLiteral(10)),ArrayCell(CallExpr(Id(r'foo'),[]),IntLiteral(3))),Assign(Id(r'a'),ArrayCell(Id(r'b'),IntLiteral(10)))],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,344))
    def test_simple_program345(self):
        input = """        
        procedure Lesson1_Program1();
        Begin
            Write("Hello World. Prepare to learn PASCAL!!");
            Readln();
        End
        """
        expect = str(Program([FuncDecl(Id(r'Lesson1_Program1'),[],[],[CallStmt(Id(r'Write'),[StringLiteral(r'Hello World. Prepare to learn PASCAL!!')]),CallStmt(Id(r'Readln'),[])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,345))
    def test_simple_program_346(self):
        input = """        
        procedure Lesson1_Program2();
        Begin
            Write("random");
            Readln();
        End
        """
        expect = str(Program([FuncDecl(Id(r'Lesson1_Program2'),[],[],[CallStmt(Id(r'Write'),[StringLiteral(r'random')]),CallStmt(Id(r'Readln'),[])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,346))

    def test_simple_program_347(self):
        input = """        
procedure foo (a , b : integer ; c : real) ;
                var x , y : real ;
                begin
                    // do your code
                end
        """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),FloatType())],[VarDecl(Id(r'x'),FloatType()),VarDecl(Id(r'y'),FloatType())],[],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,347))
    def test_simple_program_348(self):
        input = """        
            var a, b, c: integer;
            procedure main();
            begin
            a := 1 = 2;
            end
        """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),BinaryOp(r'=',IntLiteral(1),IntLiteral(2)))],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,348))
    def test_simple_program_349(self):
        input = """        
        Var  a1, a2, Sum : Integer;
    Procedure main();
    Begin {body procedure main}
        Writeln("Input 1:"); 
        Readln(a1);
        Writeln("Input 2:");
        Readln(a2);
        Sum := a1 + a2; (*addition*)
        Writeln(Sum); //show result
        Readln();
    End
        """
        expect = str(Program([VarDecl(Id(r'a1'),IntType()),VarDecl(Id(r'a2'),IntType()),VarDecl(Id(r'Sum'),IntType()),FuncDecl(Id(r'main'),[],[],[CallStmt(Id(r'Writeln'),[StringLiteral(r'Input 1:')]),CallStmt(Id(r'Readln'),[Id(r'a1')]),CallStmt(Id(r'Writeln'),[StringLiteral(r'Input 2:')]),CallStmt(Id(r'Readln'),[Id(r'a2')]),Assign(Id(r'Sum'),BinaryOp(r'+',Id(r'a1'),Id(r'a2'))),CallStmt(Id(r'Writeln'),[Id(r'Sum')]),CallStmt(Id(r'Readln'),[])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,349))

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
    def test_compound_351(self):
        input = """
                var s,r:real;i:integer;
                function expn(x:real;n:integer): real;
                begin
                    s:=1;
                    r:=1;
                    for i:=1 to n do 
                    begin
                        r:=r*x/i;
                        s:=r;
                    end
                    expn:=s;
                end"""
        expect = str(Program([VarDecl(Id(r's'),FloatType()),VarDecl(Id(r'r'),FloatType()),VarDecl(Id(r'i'),IntType()),FuncDecl(Id(r'expn'),[VarDecl(Id(r'x'),FloatType()),VarDecl(Id(r'n'),IntType())],[],[Assign(Id(r's'),IntLiteral(1)),Assign(Id(r'r'),IntLiteral(1)),For(Id(r'i'),IntLiteral(1),Id(r'n'),True,[Assign(Id(r'r'),BinaryOp(r'/',BinaryOp(r'*',Id(r'r'),Id(r'x')),Id(r'i'))),Assign(Id(r's'),Id(r'r'))]),Assign(Id(r'expn'),Id(r's'))],FloatType())]))
        self.assertTrue(TestAST.test(input,expect,351))
    def test_compound_352(self):
        input = """procedurE foo (b : real) ;
            begin
                1[1] := 1; //
                (1>=0)[5] := asd+a[1][2]+c+("abc"< 0); { asd }
                asd(1)[m+1] := 3; (* fgh *)
                (c+a[1]+(1<1))[10] := 123;
            End
            """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'b'),FloatType())],[],[Assign(ArrayCell(IntLiteral(1),IntLiteral(1)),IntLiteral(1)),Assign(ArrayCell(BinaryOp(r'>=',IntLiteral(1),IntLiteral(0)),IntLiteral(5)),BinaryOp(r'+',BinaryOp(r'+',BinaryOp(r'+',Id(r'asd'),ArrayCell(ArrayCell(Id(r'a'),IntLiteral(1)),IntLiteral(2))),Id(r'c')),BinaryOp(r'<',StringLiteral(r'abc'),IntLiteral(0)))),Assign(ArrayCell(CallExpr(Id(r'asd'),[IntLiteral(1)]),BinaryOp(r'+',Id(r'm'),IntLiteral(1))),IntLiteral(3)),Assign(ArrayCell(BinaryOp(r'+',BinaryOp(r'+',Id(r'c'),ArrayCell(Id(r'a'),IntLiteral(1))),BinaryOp(r'<',IntLiteral(1),IntLiteral(1))),IntLiteral(10)),IntLiteral(123))],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,352))
    def test_compound_353(self):
        input = """
        procedure test();
               Var 
            bool : Boolean;
            A, B : Integer;

        Begin
            A := 10;
            B := 20;
            bool := False;
            bool := (A = 10) OR (B = 10);
            Writeln(bool); 
            bool := (A = 10) AND (B = 10);
            Writeln(bool); 
        End
            """
        expect = str(Program([FuncDecl(Id(r'test'),[],[VarDecl(Id(r'bool'),BoolType()),VarDecl(Id(r'A'),IntType()),VarDecl(Id(r'B'),IntType())],[Assign(Id(r'A'),IntLiteral(10)),Assign(Id(r'B'),IntLiteral(20)),Assign(Id(r'bool'),BooleanLiteral(False)),Assign(Id(r'bool'),BinaryOp(r'OR',BinaryOp(r'=',Id(r'A'),IntLiteral(10)),BinaryOp(r'=',Id(r'B'),IntLiteral(10)))),CallStmt(Id(r'Writeln'),[Id(r'bool')]),Assign(Id(r'bool'),BinaryOp(r'AND',BinaryOp(r'=',Id(r'A'),IntLiteral(10)),BinaryOp(r'=',Id(r'B'),IntLiteral(10)))),CallStmt(Id(r'Writeln'),[Id(r'bool')])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,353))
    def test_compound_354(self):
        input = """
            function leastCommonMultiple(a, b: Integer): Integer;
            begin
            result := b * (a div greatestCommonDivisor(a, b));
            end"""
        expect = str(Program([FuncDecl(Id(r'leastCommonMultiple'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[Assign(Id(r'result'),BinaryOp(r'*',Id(r'b'),BinaryOp(r'div',Id(r'a'),CallExpr(Id(r'greatestCommonDivisor'),[Id(r'a'),Id(r'b')]))))],IntType())]))
        self.assertTrue(TestAST.test(input,expect,354))
    def test_compound_355(self):
        input = """
                function greatestCommonDivisor(a, b: Integer): Integer;
                var
                temp: Integer;
                begin
                while b <> 0 do
                begin
                    temp := b;
                    b := a mod b;
                    a := temp;
                end

                result := a;

                end"""
        expect = str(Program([FuncDecl(Id(r'greatestCommonDivisor'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[VarDecl(Id(r'temp'),IntType())],[While(BinaryOp(r'<>',Id(r'b'),IntLiteral(0)),[Assign(Id(r'temp'),Id(r'b')),Assign(Id(r'b'),BinaryOp(r'mod',Id(r'a'),Id(r'b'))),Assign(Id(r'a'),Id(r'temp'))]),Assign(Id(r'result'),Id(r'a'))],IntType())]))
        self.assertTrue(TestAST.test(input,expect,355))
    def test_compound_356(self):
        input = """
function greatestCommonDivisor_euclidsSubtractionMethod(a, b: Integer): Integer;
begin
  // only works with positive integers
  if (a < 0) then a := -a;
  if (b < 0) then b := -b;
  // don't enter loop, since subtracting zero won't break condition
  if (a = 0) then exit(b);
  if (b = 0) then exit(a);
  while not (a = b) do
  begin
    if (a > b) then
     a := a - b;
    else
     b := b - a;
  end
  result := a;
end"""
        expect = str(Program([FuncDecl(Id(r'greatestCommonDivisor_euclidsSubtractionMethod'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[If(BinaryOp(r'<',Id(r'a'),IntLiteral(0)),[Assign(Id(r'a'),UnaryOp(r'-',Id(r'a')))],[]),If(BinaryOp(r'<',Id(r'b'),IntLiteral(0)),[Assign(Id(r'b'),UnaryOp(r'-',Id(r'b')))],[]),If(BinaryOp(r'=',Id(r'a'),IntLiteral(0)),[CallStmt(Id(r'exit'),[Id(r'b')])],[]),If(BinaryOp(r'=',Id(r'b'),IntLiteral(0)),[CallStmt(Id(r'exit'),[Id(r'a')])],[]),While(UnaryOp(r'not',BinaryOp(r'=',Id(r'a'),Id(r'b'))),[If(BinaryOp(r'>',Id(r'a'),Id(r'b')),[Assign(Id(r'a'),BinaryOp(r'-',Id(r'a'),Id(r'b')))],[Assign(Id(r'b'),BinaryOp(r'-',Id(r'b'),Id(r'a')))])]),Assign(Id(r'result'),Id(r'a'))],IntType())]))
        self.assertTrue(TestAST.test(input,expect,356))
    def test_compound_357(self):
        input = """
                var a, b : integer;
                (*procedure definition *)
                procedure swap(x, y: integer); 

                var
                temp: integer;

                begin
                temp := x;
                x:= y;
                y := temp;
                end

                procedure main();
                begin
                a := 100;
                b := 200;
                writeln("Before swap, value of a : ", a );
                writeln("Before swap, value of b : ", b );
                
                swap(a, b);
                writeln("After swap, value of a : ", a );
                writeln("After swap, value of b : ", b );
                end
                        """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),FuncDecl(Id(r'swap'),[VarDecl(Id(r'x'),IntType()),VarDecl(Id(r'y'),IntType())],[VarDecl(Id(r'temp'),IntType())],[Assign(Id(r'temp'),Id(r'x')),Assign(Id(r'x'),Id(r'y')),Assign(Id(r'y'),Id(r'temp'))],VoidType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),IntLiteral(100)),Assign(Id(r'b'),IntLiteral(200)),CallStmt(Id(r'writeln'),[StringLiteral(r'Before swap, value of a : '),Id(r'a')]),CallStmt(Id(r'writeln'),[StringLiteral(r'Before swap, value of b : '),Id(r'b')]),CallStmt(Id(r'swap'),[Id(r'a'),Id(r'b')]),CallStmt(Id(r'writeln'),[StringLiteral(r'After swap, value of a : '),Id(r'a')]),CallStmt(Id(r'writeln'),[StringLiteral(r'After swap, value of b : '),Id(r'b')])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,357))
    def test_compound_358(self):
        input = """
                var
                a, b, c: integer;

                procedure main();
                begin
                (* actual initialization *)
                a := 10;
                b := 20;
                c := a + b;
                
                writeln("value of a = ", a , " b =  ",  b, " and c = ", c);
                end
        """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),IntLiteral(10)),Assign(Id(r'b'),IntLiteral(20)),Assign(Id(r'c'),BinaryOp(r'+',Id(r'a'),Id(r'b'))),CallStmt(Id(r'writeln'),[StringLiteral(r'value of a = '),Id(r'a'),StringLiteral(r' b =  '),Id(r'b'),StringLiteral(r' and c = '),Id(r'c')])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,358))
    def test_compound_359(self):
        input = """
                    var exit: boolean;
                        choice: integer;

                    procedure main();
                    begin
                    writeln("Do you want to continue? ");
                    writeln("Enter Y/y for yes, and N/n for no");
                    readln(choice);

                    if(choice = "n") then
                    exit := true;
                    else
                    exit := false;

                    if (exit) then
                    writeln(" Good Bye!");
                    else
                    writeln("Please Continue");

                    readln();
                    end
        """
        expect = str(Program([VarDecl(Id(r'exit'),BoolType()),VarDecl(Id(r'choice'),IntType()),FuncDecl(Id(r'main'),[],[],[CallStmt(Id(r'writeln'),[StringLiteral(r'Do you want to continue? ')]),CallStmt(Id(r'writeln'),[StringLiteral(r'Enter Y/y for yes, and N/n for no')]),CallStmt(Id(r'readln'),[Id(r'choice')]),If(BinaryOp(r'=',Id(r'choice'),StringLiteral(r'n')),[Assign(Id(r'exit'),BooleanLiteral(True))],[Assign(Id(r'exit'),BooleanLiteral(False))]),If(Id(r'exit'),[CallStmt(Id(r'writeln'),[StringLiteral(r' Good Bye!')])],[CallStmt(Id(r'writeln'),[StringLiteral(r'Please Continue')])]),CallStmt(Id(r'readln'),[])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,359))
    def test_compound_360(self):
        input = """       
            Var S1, S2 : String;
            Procedure main();
            Begin
                S1 := "toi";
                S2 := "la Phan Thao";
                Write(S1 + S2); { "toi la Phan Thao" }
            End
        """
        expect = str(Program([VarDecl(Id(r'S1'),StringType()),VarDecl(Id(r'S2'),StringType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'S1'),StringLiteral(r'toi')),Assign(Id(r'S2'),StringLiteral(r'la Phan Thao')),CallStmt(Id(r'Write'),[BinaryOp(r'+',Id(r'S1'),Id(r'S2'))])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,360))
    def test_compound_361(self):
        input = """
                    Var chuoi : String;

                    Procedure main();
                    Begin
                        S := "ban co khoe khong";
                        S := Copy(S, 7, 10); { "khoe!" }
                        Write(S);
                    End"""
        expect = str(Program([VarDecl(Id(r'chuoi'),StringType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'S'),StringLiteral(r'ban co khoe khong')),Assign(Id(r'S'),CallExpr(Id(r'Copy'),[Id(r'S'),IntLiteral(7),IntLiteral(10)])),CallStmt(Id(r'Write'),[Id(r'S')])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,361))
    def test_compound_362(self):
        input = """
            Procedure BubbleSort(numbers : Array[1 .. n] of Integer; size : Integer);
            Var
                i, j, tmp : Integer;

            Begin
                For i := size-1 DownTo 1 do
                    For j := 2 to i do
                        If (numbers[j-1] > numbers[j]) Then
                        Begin
                            tmp := numbers[j-1];
                            numbers[j-1] := numbers[j];
                            numbers[j] := tmp;
                        End
            End
            
        """
        expect = str(Program([FuncDecl(Id(r'BubbleSort'),[],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType()),VarDecl(Id(r'tmp'),IntType())],[For(Id(r'i'),BinaryOp(r'-',Id(r'size'),IntLiteral(1)),IntLiteral(1),False,[For(Id(r'j'),IntLiteral(2),Id(r'i'),True,[If(BinaryOp(r'>',ArrayCell(Id(r'numbers'),BinaryOp(r'-',Id(r'j'),IntLiteral(1))),ArrayCell(Id(r'numbers'),Id(r'j'))),[Assign(Id(r'tmp'),ArrayCell(Id(r'numbers'),BinaryOp(r'-',Id(r'j'),IntLiteral(1)))),Assign(ArrayCell(Id(r'numbers'),BinaryOp(r'-',Id(r'j'),IntLiteral(1))),ArrayCell(Id(r'numbers'),Id(r'j'))),Assign(ArrayCell(Id(r'numbers'),Id(r'j')),Id(r'tmp'))],[])])])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,362))
    def test_compound_363(self):
        input = """
            Procedure InsertionSort(numbers : Array[1 .. n] of Integer; size : Integer);
            Var
                i, j, index : integer;

            Begin
                For i := 2 to size-1 do
                Begin
                    index := numbers[i];
                    j := i;
                    While ((j > 1) AND (numbers[j-1] > index)) do
                    Begin
                        numbers[j] := numbers[j-1];
                        j := j - 1;
                    End
                    numbers[j] := index;
                End
            End
        """
        expect = str(Program([FuncDecl(Id(r'InsertionSort'),[],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType()),VarDecl(Id(r'index'),IntType())],[For(Id(r'i'),IntLiteral(2),BinaryOp(r'-',Id(r'size'),IntLiteral(1)),True,[Assign(Id(r'index'),ArrayCell(Id(r'numbers'),Id(r'i'))),Assign(Id(r'j'),Id(r'i')),While(BinaryOp(r'AND',BinaryOp(r'>',Id(r'j'),IntLiteral(1)),BinaryOp(r'>',ArrayCell(Id(r'numbers'),BinaryOp(r'-',Id(r'j'),IntLiteral(1))),Id(r'index'))),[Assign(ArrayCell(Id(r'numbers'),Id(r'j')),ArrayCell(Id(r'numbers'),BinaryOp(r'-',Id(r'j'),IntLiteral(1)))),Assign(Id(r'j'),BinaryOp(r'-',Id(r'j'),IntLiteral(1)))]),Assign(ArrayCell(Id(r'numbers'),Id(r'j')),Id(r'index'))])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,363))

    def test_compound_364(self):
        input = """
            Var key : String;

            Procedure main();
            Begin
                Writeln("Press \\"\\"q\\"\\" to exit...");
                key := Readkey();
                While key <> "true" do 
                Begin
                    Writeln("Please press \\"\\"true\\"\\" to exit.");
                    key := Readkey();
                End
            End
        """
        expect = str(Program([VarDecl(Id(r'key'),StringType()),FuncDecl(Id(r'main'),[],[],[CallStmt(Id(r'Writeln'),[StringLiteral(r'Press \"\"q\"\" to exit...')]),Assign(Id(r'key'),CallExpr(Id(r'Readkey'),[])),While(BinaryOp(r'<>',Id(r'key'),StringLiteral(r'true')),[CallStmt(Id(r'Writeln'),[StringLiteral(r'Please press \"\"true\"\" to exit.')]),Assign(Id(r'key'),CallExpr(Id(r'Readkey'),[]))])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,364))
    def test_compound_365(self):
        input = """        


function fact(n: integer): integer;
begin
    if (n = 0) then
        fact := 1;
    else
        fact := n * fact(n - 1);
end
procedure main();
var n: integer;

begin
    for n := 0 to 16 do
        writeln(n, "! = ", fact(n));
end
        """
        expect = str(Program([FuncDecl(Id(r'fact'),[VarDecl(Id(r'n'),IntType())],[],[If(BinaryOp(r'=',Id(r'n'),IntLiteral(0)),[Assign(Id(r'fact'),IntLiteral(1))],[Assign(Id(r'fact'),BinaryOp(r'*',Id(r'n'),CallExpr(Id(r'fact'),[BinaryOp(r'-',Id(r'n'),IntLiteral(1))])))])],IntType()),FuncDecl(Id(r'main'),[],[VarDecl(Id(r'n'),IntType())],[For(Id(r'n'),IntLiteral(0),IntLiteral(16),True,[CallStmt(Id(r'writeln'),[Id(r'n'),StringLiteral(r'! = '),CallExpr(Id(r'fact'),[Id(r'n')])])])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,365))

    def test_compound_366(self):
        input = """        
Procedure DrawLine(); 
{This procedure helps me to avoid the rewriting the for loops}
Var Counter : Integer;
Begin
	textcolor(green);
	For Counter := 1 to 10 do
	Begin 
		Write(chr(196)); 
	End
End

Procedure Main();
Begin
	GotoXy(10,5);
	DrawLine();
	GotoXy(10,6);
	DrawLine();
	GotoXy(10,7);
	DrawLine();
	GotoXy(10,10);
	DrawLine();
	Readkey();
End
        """
        expect = str(Program([FuncDecl(Id(r'DrawLine'),[],[VarDecl(Id(r'Counter'),IntType())],[CallStmt(Id(r'textcolor'),[Id(r'green')]),For(Id(r'Counter'),IntLiteral(1),IntLiteral(10),True,[CallStmt(Id(r'Write'),[CallExpr(Id(r'chr'),[IntLiteral(196)])])])],VoidType()),FuncDecl(Id(r'Main'),[],[],[CallStmt(Id(r'GotoXy'),[IntLiteral(10),IntLiteral(5)]),CallStmt(Id(r'DrawLine'),[]),CallStmt(Id(r'GotoXy'),[IntLiteral(10),IntLiteral(6)]),CallStmt(Id(r'DrawLine'),[]),CallStmt(Id(r'GotoXy'),[IntLiteral(10),IntLiteral(7)]),CallStmt(Id(r'DrawLine'),[]),CallStmt(Id(r'GotoXy'),[IntLiteral(10),IntLiteral(10)]),CallStmt(Id(r'DrawLine'),[]),CallStmt(Id(r'Readkey'),[])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,366))

    def test_compound_367(self):
        input = """        

Procedure Square(Index : Integer; Result : Integer);
Begin
	Result := Index * Index;
End

Var
	Res : Integer;

Procedure Main();
Begin
	Writeln("The square of 5 is: ");
	Square(5, Res);
	Writeln(Res);
End
        """
        expect = str(Program([FuncDecl(Id(r'Square'),[VarDecl(Id(r'Index'),IntType()),VarDecl(Id(r'Result'),IntType())],[],[Assign(Id(r'Result'),BinaryOp(r'*',Id(r'Index'),Id(r'Index')))],VoidType()),VarDecl(Id(r'Res'),IntType()),FuncDecl(Id(r'Main'),[],[],[CallStmt(Id(r'Writeln'),[StringLiteral(r'The square of 5 is: ')]),CallStmt(Id(r'Square'),[IntLiteral(5),Id(r'Res')]),CallStmt(Id(r'Writeln'),[Id(r'Res')])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,367))

    def test_compound_368(self):
        input = """        

var
   a, b, c: integer;

procedure main();
begin
   (* actual initialization *)
   a := 10;
   b := 20;
   c := a + b;
   
   writeln("value of a = ", a , " b =  ",  b, " and c = ", c);
end
        """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),IntLiteral(10)),Assign(Id(r'b'),IntLiteral(20)),Assign(Id(r'c'),BinaryOp(r'+',Id(r'a'),Id(r'b'))),CallStmt(Id(r'writeln'),[StringLiteral(r'value of a = '),Id(r'a'),StringLiteral(r' b =  '),Id(r'b'),StringLiteral(r' and c = '),Id(r'c')])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,368))

    def test_compound_369(self):
        input = """        

var
   a, b, c: integer;
procedure display();

var
   a, b, c: integer;

begin
   (* local variables *)
   a := 10;
   b := 20;
   c := a + b;
   
   writeln("Winthin the procedure display");
   writeln(" Displaying the global variables a, b, and c");
   
   writeln("value of a = ", a , " b =  ",  b, " and c = ", c);
   writeln("Displaying the local variables a, b, and c");
   
   writeln("value of a = ", a , " b =  ",  b, " and c = ", c);
end
        """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),FuncDecl(Id(r'display'),[],[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType())],[Assign(Id(r'a'),IntLiteral(10)),Assign(Id(r'b'),IntLiteral(20)),Assign(Id(r'c'),BinaryOp(r'+',Id(r'a'),Id(r'b'))),CallStmt(Id(r'writeln'),[StringLiteral(r'Winthin the procedure display')]),CallStmt(Id(r'writeln'),[StringLiteral(r' Displaying the global variables a, b, and c')]),CallStmt(Id(r'writeln'),[StringLiteral(r'value of a = '),Id(r'a'),StringLiteral(r' b =  '),Id(r'b'),StringLiteral(r' and c = '),Id(r'c')]),CallStmt(Id(r'writeln'),[StringLiteral(r'Displaying the local variables a, b, and c')]),CallStmt(Id(r'writeln'),[StringLiteral(r'value of a = '),Id(r'a'),StringLiteral(r' b =  '),Id(r'b'),StringLiteral(r' and c = '),Id(r'c')])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,369))

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
    def test_Dijiks_372(self):
        input = """
        procedure Dijkstra();
        var i,k,j: integer;
        begin
        for k :=  1 to n do
        begin
        i :=  Min; { tim dinh i co trong so p[i] -> min }
        d[i] :=  1; {danh dau dinh i la da xu li }
        for j :=  1 to n do
            if d[j] = 0 then {dinh chua tham }
        if a[i][j] > 0 then {co duong di i -> j }
                    if p[i] + a[i][j] < p[j] then
                begin {sua dinh }
                p[j] :=  p[i] + a[i][j];
                before[j] :=  i;
            end
        end
        end"""
        expect = str(Program([FuncDecl(Id(r'Dijkstra'),[],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'k'),IntType()),VarDecl(Id(r'j'),IntType())],[For(Id(r'k'),IntLiteral(1),Id(r'n'),True,[Assign(Id(r'i'),Id(r'Min')),Assign(ArrayCell(Id(r'd'),Id(r'i')),IntLiteral(1)),For(Id(r'j'),IntLiteral(1),Id(r'n'),True,[If(BinaryOp(r'=',ArrayCell(Id(r'd'),Id(r'j')),IntLiteral(0)),[If(BinaryOp(r'>',ArrayCell(ArrayCell(Id(r'a'),Id(r'i')),Id(r'j')),IntLiteral(0)),[If(BinaryOp(r'<',BinaryOp(r'+',ArrayCell(Id(r'p'),Id(r'i')),ArrayCell(ArrayCell(Id(r'a'),Id(r'i')),Id(r'j'))),ArrayCell(Id(r'p'),Id(r'j'))),[Assign(ArrayCell(Id(r'p'),Id(r'j')),BinaryOp(r'+',ArrayCell(Id(r'p'),Id(r'i')),ArrayCell(ArrayCell(Id(r'a'),Id(r'i')),Id(r'j')))),Assign(ArrayCell(Id(r'before'),Id(r'j')),Id(r'i'))],[])],[])],[])])])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,372))
    def test_Primechk_373(self):
        input = """
function Primechk():integer;
Var 
Num                     :       Integer; 
checker,count,adder     :       integer; 
Begin 
 Write("Enter one number : "); 
 Readln(Num); 
 adder := 0; 
 For count := 1 to 10 do 
   begin 
     checker := num mod count; 
     if checker = 0 then 
     adder := adder + 1 ;
   end
 if (num <= 10) and (adder > 2) then 
    Writeln(num, " is not a prime number") ;
 else 
     if (num > 10) and (adder > 1) then 
        Writeln(num, " is not a prime number") ;
     else 
         Writeln(num," is a prime number"); 
end"""
        expect = str(Program([FuncDecl(Id(r'Primechk'),[],[VarDecl(Id(r'Num'),IntType()),VarDecl(Id(r'checker'),IntType()),VarDecl(Id(r'count'),IntType()),VarDecl(Id(r'adder'),IntType())],[CallStmt(Id(r'Write'),[StringLiteral(r'Enter one number : ')]),CallStmt(Id(r'Readln'),[Id(r'Num')]),Assign(Id(r'adder'),IntLiteral(0)),For(Id(r'count'),IntLiteral(1),IntLiteral(10),True,[Assign(Id(r'checker'),BinaryOp(r'mod',Id(r'num'),Id(r'count'))),If(BinaryOp(r'=',Id(r'checker'),IntLiteral(0)),[Assign(Id(r'adder'),BinaryOp(r'+',Id(r'adder'),IntLiteral(1)))],[])]),If(BinaryOp(r'and',BinaryOp(r'<=',Id(r'num'),IntLiteral(10)),BinaryOp(r'>',Id(r'adder'),IntLiteral(2))),[CallStmt(Id(r'Writeln'),[Id(r'num'),StringLiteral(r' is not a prime number')])],[If(BinaryOp(r'and',BinaryOp(r'>',Id(r'num'),IntLiteral(10)),BinaryOp(r'>',Id(r'adder'),IntLiteral(1))),[CallStmt(Id(r'Writeln'),[Id(r'num'),StringLiteral(r' is not a prime number')])],[CallStmt(Id(r'Writeln'),[Id(r'num'),StringLiteral(r' is a prime number')])])])],IntType())]))
        self.assertTrue(TestAST.test(input,expect,373))
    def test_complex_program_374(self):
        input = """
  VAR First,  Second, Left, Right: BOOLEAN;
  PROCEDURE  WriteBool(Val: BOOLEAN);
  BEGIN
  IF Val THEN
  Write("TRUE ");
  ELSE
  Write("FALSE ");
  END { WriteBool  }
  PROCEDURE Main();
  BEGIN
  { Write Header }
  WriteLn("Proof  of DeMorgan theorem ");
  WriteLn();
  WriteLn("First  Second Left Right ");
  WriteLn("-----  ------ ----- ----- ");
  { Loop through  all truth value combinations }
  FOR First :=  FALSE TO TRUE DO
  FOR Second :=  FALSE TO TRUE DO BEGIN
  { Write out  Input values of First, Second }
  WriteBool(First);
  WriteBool(Second);
  { Separate Input  values from the output }
  Write(" ");
  Left := (NOT  First) AND (NOT Second);
  Right := NOT(First OR Second);
  { Write out the  new values of Left, Right }
  WriteBool(Left);
  WriteBool(Right);
  WriteLn();
  END { Inner FOR  }
  END { TruthTable  }"""
        expect = str(Program([VarDecl(Id(r'First'),BoolType()),VarDecl(Id(r'Second'),BoolType()),VarDecl(Id(r'Left'),BoolType()),VarDecl(Id(r'Right'),BoolType()),FuncDecl(Id(r'WriteBool'),[VarDecl(Id(r'Val'),BoolType())],[],[If(Id(r'Val'),[CallStmt(Id(r'Write'),[StringLiteral(r'TRUE ')])],[CallStmt(Id(r'Write'),[StringLiteral(r'FALSE ')])])],VoidType()),FuncDecl(Id(r'Main'),[],[],[CallStmt(Id(r'WriteLn'),[StringLiteral(r'Proof  of DeMorgan theorem ')]),CallStmt(Id(r'WriteLn'),[]),CallStmt(Id(r'WriteLn'),[StringLiteral(r'First  Second Left Right ')]),CallStmt(Id(r'WriteLn'),[StringLiteral(r'-----  ------ ----- ----- ')]),For(Id(r'First'),BooleanLiteral(False),BooleanLiteral(True),True,[For(Id(r'Second'),BooleanLiteral(False),BooleanLiteral(True),True,[CallStmt(Id(r'WriteBool'),[Id(r'First')]),CallStmt(Id(r'WriteBool'),[Id(r'Second')]),CallStmt(Id(r'Write'),[StringLiteral(r' ')]),Assign(Id(r'Left'),BinaryOp(r'AND',UnaryOp(r'NOT',Id(r'First')),UnaryOp(r'NOT',Id(r'Second')))),Assign(Id(r'Right'),UnaryOp(r'NOT',BinaryOp(r'OR',Id(r'First'),Id(r'Second')))),CallStmt(Id(r'WriteBool'),[Id(r'Left')]),CallStmt(Id(r'WriteBool'),[Id(r'Right')]),CallStmt(Id(r'WriteLn'),[])])])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,374))
    def test_complex_program_375(self):
        input = """
        var t: integer;
        f: string;
        procedure Hn(n,a,b: integer);
            begin
            if n = 0 then exit();
            Hn(n-1,a,6-a-b);
            inc(d);
            writeln(f,t,". ",a," -> ",b);
            Hn(n-1,6-a-b,b);
            end
        procedure runHn(n: integer);
            begin
            d :=  0;
            assign(f,"hanoi.out");
            rewrite(f);
            writeln("-----------------");
            Hn(n,1,2);
            writeln(f,"Total: ",d," step(s)");
            close(f);
            readln();
            end
        procedure main();
        BEGIN
        runHn(3);
        END"""
        expect = str(Program([VarDecl(Id(r't'),IntType()),VarDecl(Id(r'f'),StringType()),FuncDecl(Id(r'Hn'),[VarDecl(Id(r'n'),IntType()),VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[If(BinaryOp(r'=',Id(r'n'),IntLiteral(0)),[CallStmt(Id(r'exit'),[])],[]),CallStmt(Id(r'Hn'),[BinaryOp(r'-',Id(r'n'),IntLiteral(1)),Id(r'a'),BinaryOp(r'-',BinaryOp(r'-',IntLiteral(6),Id(r'a')),Id(r'b'))]),CallStmt(Id(r'inc'),[Id(r'd')]),CallStmt(Id(r'writeln'),[Id(r'f'),Id(r't'),StringLiteral(r'. '),Id(r'a'),StringLiteral(r' -> '),Id(r'b')]),CallStmt(Id(r'Hn'),[BinaryOp(r'-',Id(r'n'),IntLiteral(1)),BinaryOp(r'-',BinaryOp(r'-',IntLiteral(6),Id(r'a')),Id(r'b')),Id(r'b')])],VoidType()),FuncDecl(Id(r'runHn'),[VarDecl(Id(r'n'),IntType())],[],[Assign(Id(r'd'),IntLiteral(0)),CallStmt(Id(r'assign'),[Id(r'f'),StringLiteral(r'hanoi.out')]),CallStmt(Id(r'rewrite'),[Id(r'f')]),CallStmt(Id(r'writeln'),[StringLiteral(r'-----------------')]),CallStmt(Id(r'Hn'),[Id(r'n'),IntLiteral(1),IntLiteral(2)]),CallStmt(Id(r'writeln'),[Id(r'f'),StringLiteral(r'Total: '),Id(r'd'),StringLiteral(r' step(s)')]),CallStmt(Id(r'close'),[Id(r'f')]),CallStmt(Id(r'readln'),[])],VoidType()),FuncDecl(Id(r'main'),[],[],[CallStmt(Id(r'runHn'),[IntLiteral(3)])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,375))
    def test_short_program_376(self):
        input = """
        var a,b,c: integer; d:boolean; r:real;
        procedure main();
        begin
            a:= 1;
            b:= 3;
            c:= 6;
            d:= true;
            r:= 1.25;
            sum(a,b,c);
        end
        """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'd'),BoolType()),VarDecl(Id(r'r'),FloatType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),IntLiteral(1)),Assign(Id(r'b'),IntLiteral(3)),Assign(Id(r'c'),IntLiteral(6)),Assign(Id(r'd'),BooleanLiteral(True)),Assign(Id(r'r'),FloatLiteral(1.25)),CallStmt(Id(r'sum'),[Id(r'a'),Id(r'b'),Id(r'c')])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,376))
    def test_short_program_377(self):
        input = """
        var a,b,c: integer; d:boolean; r:real;
        procedure main();
        begin
            a:= 1;
            b:= 1;
            c:= 1;
            d:= true;
            r:= 1.25;
            sum(a,b,c);
            if a = sum(a,b,c) then
                d:= false;
        end
        """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'd'),BoolType()),VarDecl(Id(r'r'),FloatType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),IntLiteral(1)),Assign(Id(r'b'),IntLiteral(1)),Assign(Id(r'c'),IntLiteral(1)),Assign(Id(r'd'),BooleanLiteral(True)),Assign(Id(r'r'),FloatLiteral(1.25)),CallStmt(Id(r'sum'),[Id(r'a'),Id(r'b'),Id(r'c')]),If(BinaryOp(r'=',Id(r'a'),CallExpr(Id(r'sum'),[Id(r'a'),Id(r'b'),Id(r'c')])),[Assign(Id(r'd'),BooleanLiteral(False))],[])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,377))
    def test_short_program_378(self):
        input = """
        var a,b,c: integer; d:boolean; r:real;
        procedure main();
        begin
            a:= 1;
            b:= 1;
            c:= 1;
            d:= true;
            r:= 1.25;
            sum(a,b,c);
            if a = sum(a,b,c) then
                d:= false;
            else 
                a := a + 2;
            Writeln("Chuong trinh nham");
        end
        """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'd'),BoolType()),VarDecl(Id(r'r'),FloatType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),IntLiteral(1)),Assign(Id(r'b'),IntLiteral(1)),Assign(Id(r'c'),IntLiteral(1)),Assign(Id(r'd'),BooleanLiteral(True)),Assign(Id(r'r'),FloatLiteral(1.25)),CallStmt(Id(r'sum'),[Id(r'a'),Id(r'b'),Id(r'c')]),If(BinaryOp(r'=',Id(r'a'),CallExpr(Id(r'sum'),[Id(r'a'),Id(r'b'),Id(r'c')])),[Assign(Id(r'd'),BooleanLiteral(False))],[Assign(Id(r'a'),BinaryOp(r'+',Id(r'a'),IntLiteral(2)))]),CallStmt(Id(r'Writeln'),[StringLiteral(r'Chuong trinh nham')])],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,378))
    def test_short_program_379(self):
        input = """
        var a,b,c: integer; d:boolean; r:real;arr:array[1 .. 20] of integer;
        procedure main();
        begin
            Writeln("Khai bao bien");
            arr[1] := a;
            arr[2] := b;
            arr[3] := c;
        end
        """
        expect = str(Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'd'),BoolType()),VarDecl(Id(r'r'),FloatType()),VarDecl(Id(r'arr'),ArrayType(1,20,IntType())),FuncDecl(Id(r'main'),[],[],[CallStmt(Id(r'Writeln'),[StringLiteral(r'Khai bao bien')]),Assign(ArrayCell(Id(r'arr'),IntLiteral(1)),Id(r'a')),Assign(ArrayCell(Id(r'arr'),IntLiteral(2)),Id(r'b')),Assign(ArrayCell(Id(r'arr'),IntLiteral(3)),Id(r'c'))],VoidType())]))
        self.assertTrue(TestAST.test(input,expect,379))
    def test_statements_380(self):
        input = """
        function foo (a,b:integer):real; begin
            read(true);
            while true and false do
            if a<c then return 1;
            else a:=a+c;
        end
        function foo (a,b:integer):real; begin
            read(true);
            for i := 1 to true+false do
                begin
                    a:=a+1;
                end
        end
        """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[CallStmt(Id(r'read'),[BooleanLiteral(True)]),While(BinaryOp(r'and',BooleanLiteral(True),BooleanLiteral(False)),[If(BinaryOp(r'<',Id(r'a'),Id(r'c')),[Return(IntLiteral(1))],[Assign(Id(r'a'),BinaryOp(r'+',Id(r'a'),Id(r'c')))])])],FloatType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[CallStmt(Id(r'read'),[BooleanLiteral(True)]),For(Id(r'i'),IntLiteral(1),BinaryOp(r'+',BooleanLiteral(True),BooleanLiteral(False)),True,[Assign(Id(r'a'),BinaryOp(r'+',Id(r'a'),IntLiteral(1)))])],FloatType())]))
        self.assertTrue(TestAST.test(input,expect,380))
    def test_expr_index_nested_381(self):
        input = """
        function foo (a,b:integer):real; 
        begin
            return a[b[c]];
        end
        """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[Return(ArrayCell(Id(r'a'),ArrayCell(Id(r'b'),Id(r'c'))))],FloatType())]))
        self.assertTrue(TestAST.test(input,expect,381))
    def test_expr_index_nested_382(self):
        input = """
        function foo (a,b:integer):real; begin
            a[1[true]] := b[false[2]] :=1;
        end
        """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[Assign(ArrayCell(Id(r'b'),ArrayCell(BooleanLiteral(False),IntLiteral(2))),IntLiteral(1)),Assign(ArrayCell(Id(r'a'),ArrayCell(IntLiteral(1),BooleanLiteral(True))),ArrayCell(Id(r'b'),ArrayCell(BooleanLiteral(False),IntLiteral(2))))],FloatType())]))
        self.assertTrue(TestAST.test(input,expect,382))

    def test_invo_nested_383(self):
        input = """
        function foo (a,b:integer):real; begin
            return a(b(c));  
        end
        """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[Return(CallExpr(Id(r'a'),[CallExpr(Id(r'b'),[Id(r'c')])]))],FloatType())]))
        self.assertTrue(TestAST.test(input,expect,383))
    def test_invo_nested_384(self):
        input = """
        function foo (a,b:integer):real; begin
            a := b(c(d));
        end
        """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[Assign(Id(r'a'),CallExpr(Id(r'b'),[CallExpr(Id(r'c'),[Id(r'd')])]))],FloatType())]))
        self.assertTrue(TestAST.test(input,expect,384))


    def test_assign_complex_385(self):
        input = """
        function foo (a,b:integer):real; 
        begin
            a := bar(TrUe,falsE)[true] := 1;  
        end
        """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[Assign(ArrayCell(CallExpr(Id(r'bar'),[BooleanLiteral(True),BooleanLiteral(False)]),BooleanLiteral(True)),IntLiteral(1)),Assign(Id(r'a'),ArrayCell(CallExpr(Id(r'bar'),[BooleanLiteral(True),BooleanLiteral(False)]),BooleanLiteral(True)))],FloatType())]))
        self.assertTrue(TestAST.test(input,expect,385))
    def test_if_nested_386(self):
        input = """
        function foo (a,b:integer):real; 
        begin
            if true<false
            then
                if a<b[2]
                then return 1;
            else
                a:= b[3];
        end
        """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[If(BinaryOp(r'<',BooleanLiteral(True),BooleanLiteral(False)),[If(BinaryOp(r'<',Id(r'a'),ArrayCell(Id(r'b'),IntLiteral(2))),[Return(IntLiteral(1))],[Assign(Id(r'a'),ArrayCell(Id(r'b'),IntLiteral(3)))])],[])],FloatType())]))
        self.assertTrue(TestAST.test(input,expect,386))

    def test_if_387(self):
        input = """
        function foo (a,b:integer):real; 
        begin
            if 1
            then
                if 2
                then 
                    if 3
                    then
                        if 4
                        then
                            return 4;
            else
                return 5;
        end
        """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[If(IntLiteral(1),[If(IntLiteral(2),[If(IntLiteral(3),[If(IntLiteral(4),[Return(IntLiteral(4))],[Return(IntLiteral(5))])],[])],[])],[])],FloatType())]))
        self.assertTrue(TestAST.test(input,expect,387))

    def test_while_nested_388(self):
        input = """
        function foo (a,b:integer):real; begin
            while a<b
            do 
                while a<c
                do a[i]:=i;
        end
        """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[While(BinaryOp(r'<',Id(r'a'),Id(r'b')),[While(BinaryOp(r'<',Id(r'a'),Id(r'c')),[Assign(ArrayCell(Id(r'a'),Id(r'i')),Id(r'i'))])])],FloatType())]))
        self.assertTrue(TestAST.test(input,expect,388))

    def test_while_389(self):
        input = """
        function foo (a,b:integer):real; begin
            while 1
            do
                while 2
                do
                    while 3
                    do
                        while 4
                        do a:=1;
        end
        """
        expect = str(Program([FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[While(IntLiteral(1),[While(IntLiteral(2),[While(IntLiteral(3),[While(IntLiteral(4),[Assign(Id(r'a'),IntLiteral(1))])])])])],FloatType())]))
        self.assertTrue(TestAST.test(input,expect,389))

