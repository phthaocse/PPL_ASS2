from MPVisitor import MPVisitor
from MPParser import MPParser
from AST import *

class ASTGeneration(MPVisitor):
    def visitProgram(self,ctx:MPParser.ProgramContext):
        return Program([self.visit(x) for x in ctx.decl()])

    def visitDecl(self,ctx:MPParser.DeclContext):
    #decl: var_dec | fun_dec | procedure_dec 
        return Decl(self.visitChild(ctx))

    def visitVardecl(self,ctx:MPParser.Var_decContext):
    # VAR varlist_dec
        return self.visit(ctx.varlist_dec())

    def visitVarlist(self,ctx:MPParser.Varlist_decContext):        
    # varlist_dec: one_var_dec varlist_dec | one_var_dec ; 
        result = []
        while(ctx.getChildCount() != 1):
            result.insert(len(result),self.visit(ctx.one_var_dec()))
            ctx = ctx.varlist_dec()
        result.insert(len(result),self.visit(ctx.one_var_dec()))
        return [self.visit(x) for x in result]

    def visitOne_var_dec(self,ctx:MPParser.One_var_decContext):
    #one_var_dec:  idlist COLON types  SEMI 
        id_l = self.visit(ctx.idlist())
        return [VarDecl(x,ctx.types()) for x in id_l]

    def visitIdlist(self,ctx:MPParser.IdlistContext):
    #idlist: ID COMMA idlist | ID;
        result = []
        while(ctx.getChildCount() != 1):
            result.insert(len(result),Id(ctx.ID().getText()))
            ctx = ctx.idlist()
        result.insert(len(result),Id(ctx.ID().getText()))
        return result


    def visitFun_dec(self, ctx:MPParser.Fun_decContext):
    #  fun_dec: FUNCTION ID LB paralist RB COLON types SEMI (var_dec)? compoundStatement
        para = self.visit(ctx.paralist())
        local = self.visit(ctx.var_dec())
        cpstmt = self.visit(ctx.compoundStatement())
        return FuncDecl(Id(ctx.ID().getText()),
                        para,
                        local,
                        cpstmt,
                        self.visit(ctx.mtype()))

    def visitProcdecl(self,ctx:MPParser.ProcdeclContext):
    #procedure_dec: PROCEDURE ID LB paralist RB SEMI var_dec? compoundStatement ;
        para = self.visit(ctx.paralist())
        local = self.visit(ctx.var_dec())
        cpstmt = self.visit(ctx.compoundStatement())
        return FuncDecl(Id(ctx.ID().getText()),
                        para,
                        local,
                        cpstmt)
    def visitParalist(self, ctx:MPParser.ParalistContext):
    #paralist: para_dec SEMI paralist | (para_dec)? 
        result = [] #list store para_dec
        while(ctx.getChildCount() != 1):
            result.insert(len(result),ctx.para_dec)
            ctx = ctx.paralist()
        result.insert(len(result),ctx.para_dec)
        return [self.visit(x) for x in result]

    def visitPara_dec(self, ctx:MPParser.Para_decContext):
    #para_dec: idlist COLON types
        id_l = self.visit(ctx.idlist())
        return [VarDecl(x,ctx.types()) for x in id_l]

    def visitTypes(self, ctx:MPParser.TypesContext):
    #types: primitive_types| compound_type 
        return Type(self.visitChild(ctx))

    def visitLiterals(self, ctx:MPParser.LiteralsContext):
    """    literals
    : INTLIT 
    | FLOATLIT
    | BOOL_LIT
    | STRING_LIT
    ;
    """
        if self.visitChild(ctx) == ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT()))
        elif self.visitChild(ctx) == ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT()))
        elif self.visitChild(ctx) == ctx.BOOL_LIT():
            return BooleanLiteral(bool(ctx.BOOL_LIT()))
        else 
            return StringLiteral(string(ctx.STRING_LIT()))

    def visitPrimitive_types(self, ctx:MPParser.Primitive_typesContext):
    #primitive_types: ( BOOLEAN | INTEGER | REAL | STRING )
        if self.visitChild(ctx) == ctx.BOOLEAN():
            return BoolType()
        elif self.visitChild(ctx) == ctx.INTEGER()
            return IntType()
        elif self.visitChild(ctx) == ctx.REAL()
            return FloatType()
        else
            return StringType()

    def visitCompound_type(self, ctx:MPParser.Compound_typeContext):    
    #compound_type: array_dec
        self.visitChild(ctx.array_dec())
        return ArrayType()

    def visitArray_dec(self, ctx:MPParser.Array_decContext):
    #array_dec: ARRAY LSB expression DD2 expression RSB OF primitive_types 

    def visitOperand(self, ctx:MPParser.OperandContext):
    """operand
    : literals
    | ID
    | funcall
    ;"""
        if self.visitChild(ctx) == ctx.literals():
            return self.visitLiterals(ctx.literals())
        elif self.visitChild(ctx) == ctx.ID():
            return Id(ctx.ID().getText())
        else 
            return self.visitFuncall(ctx.funcall())

    def visitFuncall(self, ctx:MPParser.FuncallContext):
    #funcall: ID LB listexp? RB 
        return CallExpr(Id(ctx.ID().getText()),self.visit(ctx.listexp()))

    def visitListexp(self, ctx:MPParser.ListexpContext):
    #listexp: expression COMMA listexp | expression
        result = [] #list store exp (listexp)
        while ctx.getChildCount() != 1
            result.insert(len(result),self.visit(ctx.expression()))
            ctx = ctx.listexp() 
        result.insert(len(result),self.visit(ctx.expression()))
        return result

    def visitCompoundStatement(self, ctx:MPParser.CompoundStatementContext):
    #compoundStatement: BEGIN (lis_statements)? END 
        return self.visit(ctx.lis_statements())

    def visitStatements(self, ctx:MPParser.StatementsContext):
""" statements
    : assignstatement
    | ifstatement
    | whilestatement
    | forstatement
    | breakstatement
    | continuestatement
    | returnstatement
    | compoundStatement
    | withstatements
    | callstatements
    ;"""
        return self.visitChild(ctx)
    


    def visitBody(self,ctx:MPParser.BodyContext):
        return [],[self.visit(ctx.stmt())] if ctx.stmt() else []
  
    def visitStmt(self,ctx:MPParser.StmtContext):
        return self.visit(ctx.funcall())

    def visitFuncall(self,ctx:MPParser.FuncallContext):
        return CallStmt(Id(ctx.ID().getText()),[self.visit(ctx.exp())] if ctx.exp() else [])

    def visitExp(self,ctx:MPParser.ExpContext):
        return IntLiteral(int(ctx.INTLIT().getText()))

    def visitMtype(self,ctx:MPParser.MtypeContext):
        return IntType()
        

