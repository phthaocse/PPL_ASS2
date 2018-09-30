from MPVisitor import MPVisitor
from MPParser import MPParser
from AST import *

class ASTGeneration(MPVisitor):
    def visitProgram(self,ctx:MPParser.ProgramContext):
        return Program([self.visit(x) for x in ctx.decl()])

    def visitDecl(self,ctx:MPParser.DeclContext):
        return Decl(visitChild(ctx))

    def visitVardecl(self,ctx:MPParser.Var_decContext):
    # VAR varlist_dec
        return self.visit(ctx.varlist_dec())

    def visitVarlist(self,ctx:MPParser.Varlist_decContext):        
    # varlist_dec: one_var_dec varlist_dec | one_var_dec ; 
        result = [None]
        while(ctx.getChildCount() != 1):
            result.insert(len(result),visit(ctx.one_var_dec()))
            ctx = ctx.varlist_dec()
        result.insert(len(result),visit(ctx.one_var_dec()))
        return [self.visit(x) for x in result]

    def visitOne_var_dec(self,ctx:MPParser.One_var_decContext):
    #one_var_dec:  idlist COLON types  SEMI 
        id_l = self.visit(ctx.idlist())
        return [VarDecl(x,ctx.types()) for x in id_l]

    def visitIdlist(self,ctx:MPParser.IdlistContext):
    #idlist: ID COMMA idlist | ID;
        result = [None]
        while(ctx.getChildCount() != 1):
            result.insert(len(result),ctx.ID().getText())
            ctx = ctx.idlist()
        result.insert(len(result),ctx.ID().getText())
        return result


    def visitFun_dec(self, ctx:MPParser.Fun_decContext):
    #   fun_dec: FUNCTION ID LB paralist RB COLON types SEMI (var_dec)? compoundStatement
        para = self.visit(ctx.paralist())
        local = self.visit(ctx.var_dec())
        cpstmt = self.visit(ctx.compoundStatement())
        return FuncDecl(ctx.ID().getText()),
                        para,
                        local,
                        cpstmt,
                        self.visit(ctx.mtype())

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
        

