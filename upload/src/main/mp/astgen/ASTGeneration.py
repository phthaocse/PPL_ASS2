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
`  """
        if self.visitChild(ctx) == ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT()))
        elif self.visitChild(ctx) == ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT()))
        elif self.visitChild(ctx) == ctx.BOOL_LIT():
            return BooleanLiteral(bool(ctx.BOOL_LIT()))
        else: 
            return StringLiteral(string(ctx.STRING_LIT()))

    def visitPrimitive_types(self, ctx:MPParser.Primitive_typesContext):
    #primitive_types: ( BOOLEAN | INTEGER | REAL | STRING )
        if self.visitChild(ctx) == ctx.BOOLEAN():
            return BoolType()
        elif self.visitChild(ctx) == ctx.INTEGER()
            return IntType()
        elif self.visitChild(ctx) == ctx.REAL()
            return FloatType()
        else:
            return StringType()

    def visitCompound_type(self, ctx:MPParser.Compound_typeContext):    
    #compound_type: array_dec
        self.visitChild(ctx.array_dec())

    def visitArray_dec(self, ctx:MPParser.Array_decContext):
    #array_dec: ARRAY LSB expression DD2 expression RSB OF primitive_types 
        return ArrayType(self.visit(ctx.expression()),self.visit(ctx.expression()),self.visit(ctx.primitive_types()))

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
        else: 
            return self.visitFuncall(ctx.funcall())

    """expression:
    expression ANDTHEN expression1
    | expression ORELSE expression1
    | expression1
    | operand
    ;"""
    def visitExpression(self, ctx:MPParser.ExpressionContext):
        if ctx.getChildCount() == 1:
            return self.visitChild(ctx)
        elif ctx.getChild(1) == ctx.ANDTHEN():
            andthen = "andthen"
            return BinaryOp(andthen,self.visit(ctx.expression()),self.visit(ctx.expression1()))
        else 
            orelse = "orelse" 
            return BinaryOp(orelse,self.visit(ctx.expression()),self.visit(ctx.expression1()))

    """expression1:
    expression2 EQUAL expression2
    | expression2 NOT_EQUAL expression2
    | expression2 LESS_THAN expression2
    | expression2 GREATER_THAN expression2
    | expression2 LESS_THAN_EQUAL expression2
    | expression2 GREATER_THAN_EQUAL expression2
    | expression2
    ;"""
    def visitExpression1(self, ctx:MPParser.Expression1Context):
        if ctx.getChildCount() == 1:
            self.visitChild(ctx)
        else
            return BinaryOp(ctx.getChild(1).getText(),self.visit(ctx.expression2()),self.visit(ctx.expression2()))

    """expression2:
    expression2 ADD expression3
    | expression2 SUB expression3
    | expression2 OR expression3
    | expression3
    ;"""
    def visitExpression2(self, ctx:MPParser.Expression2Context):
        if ctx.getChildCount() == 1:
            self.visitChild(ctx)
        else
            return BinaryOp(ctx.getChild(1).getText(),self.visit(ctx.expression2()),self.visit(ctx.expression3()))

    """expression3:
    expression3 DIVISION expression4
    | expression3 MULTIPLICATION expression4
    | expression3 DIV expression4
    | expression3 MOD expression4
    | expression3 AND expression4
    | expression4
    ;"""
    def visitExpression3(self, ctx:MPParser.Expression3Context):
        if ctx.getChildCount() == 1:
            self.visitChild(ctx)
        else
            return BinaryOp(ctx.getChild(1).getText(),self.visit(ctx.expression3()),self.visit(ctx.expression4()))

    """expression4:
    SUB expression4
    | NOT expression4
    | expression5
    ;"""
    def visitExpression4(self, ctx:MPParser.Expression4Context):
        if ctx.getChildCount() == 1:
            self.visitChild(ctx)
        else
            return UnaryOp(ctx.getChild(0).getText(),self.visit(ctx.expression4()))        

    """expression5:
    expression5 LSB expression RSB
    | expression6
    ;"""
    def visitExpression5(self, ctx:MPParser.Expression5Context):
        if ctx.getChildCount() == 1:
            self.visitChild(ctx)
        else 
            return ArrayCell(self.visit(ctx.expression5()),self.visit(ctx.expression()))        

    """expression6:
    LB expression RB
    | operand
    ;"""
    def visitExpression6(self, ctx:MPParser.Expression6Context):
        if ctx.getChildCount() == 1:
            self.visitChild(ctx)
        else
            self.visit(ctx.expression())

    """arrayelement:
    expression5 LSB expression RSB
    ;"""
    def visitArrayelement(self, ctx:MPParser.ArrayelementContext):
            if ctx.getChildCount() == 1:
            self.visitChild(ctx)
        else 
            return ArrayCell(self.visit(ctx.expression5()),self.visit(ctx.expression()))  

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
    def visitStatements(self, ctx:MPParser.StatementsContext):
        return self.visitChild(ctx)

    def visitAssignstatement(self, ctx:MPParser.AssignstatementContext):
    #assignstatement: (variable ASSIGN)+ expression SEMI 
        var_list = [self.visit(x) for x in ctx.variable()]
        return [Assign(x,self.visit(ctx.expression())) for x in var_list]

    def visitVariable(self, ctx:MPParser.VariableContext):
    #variable: ID | arrayelement
        if self.visitChild(ctx) == ctx.ID():
            return Id(ctx.ID().getText())
        else:
            self.visitChild(ctx)

    def visitIfstatement(self, ctx:MPParser.IfstatementContext):
    #ifstatement: IF expression THEN statements (: ELSE statements)? 
        return If(self.visit(ctx.expression()),self.visit(ctx.statements()),self.visit(ctx.statements()))

    def visitWhilestatement(self, ctx:MPParser.WhilestatementContext):
    #whilestatement: WHILE expression DO  statements 
        return While(self.visit(ctx.expression()),self.visit(ctx.statements()))

    def visitForstatement(self, ctx:MPParser.ForstatementContext):
    #forstatement: FOR ID ASSIGN initialExp (TO | DOWNTO) finalExp DO statements 
        if ctx.getChild(4) == ctx.TO():
            up = True
        else:
            up = False
        return For(Id(ctx.ID().getText()),self.visit(ctx.initialExp()),self.visit(ctx.finalExp()),up,self.visit(ctx.statements()))        

    def visitInitialExp(self, ctx:MPParser.InitialExpContext):
    #initialExp: expression
        return self.visitChild(ctx)

    def visitFinalExp(self, ctx:MPParser.FinalExpContext):
        return self.visitChild(ctx)

    def visitBreakstatement(self, ctx:MPParser.BreakstatementContext):
    #breakstatement: BREAK SEMI 
        return Break()

    def visitContinuestatement(self, ctx:MPParser.ContinuestatementContext):
    #continuestatement: CONTINUE SEMI 
        return Continue()

    def visitReturnstatement(self, ctx:MPParser.ReturnstatementContext):
    #returnstatement: RETURN expression? SEMI 
        return Return(self.visit(ctx.expression()))
        
    def visitLis_statements(self, ctx:MPParser.Lis_statementsContext):
    #lis_statements: statements lis_statements | statements ;
        result = [] #lis_stmt
        while ctx.getChildCount() != 1
            result.insert(len(result),ctx.statements())
            ctx = ctx.lis_statements()
        result.insert(len(result),ctx.statements())
        return result

    def visitWithstatements(self, ctx:MPParser.WithstatementsContext):
    #withstatements: WITH varlist_dec DO statements
        return With(self.visit(ctx.varlist_dec()),self.visit(ctx.statements()))

    def visitCallstatements(self, ctx:MPParser.CallstatementsContext):
    #callstatements: funcall SEMI 
        ctx = self.visit(ctx.funcall())
        return CallStmt(Id(ctx.ID().getText()),self.visit(ctx.listexp()))

