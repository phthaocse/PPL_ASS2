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
        expect = "Program([VarDecl(Id(i),IntType),VarDecl(Id(j),FloatType),VarDecl(Id(k),FloatType),FuncDecl(Id(main),[],VoidType(),[],[])])"
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
    def test_simple_program309(self):
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