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