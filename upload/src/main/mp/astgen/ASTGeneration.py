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
        return [self.visit(ctx.varlist_dec())]
    def visitVarlist(self,ctx:MPParser.Varlist_decContext):        
    # varlist_dec: one_var_dec varlist_dec | one_var_dec ; 
        if(ctx.getChildCount() == 1)
            return [self.visit(ctx.one_var_dec())]
        else
            return self.visit(ctx.one_var_dec()) & visitVarlist(self,ctx.varlist_dec())
    def visitOne_var_dec(self,ctx:MPParser.One_var_decContext)
    #one_var_dec:  idlist COLON types  SEMI 
        return VarDecl(self.visit(ctx.idlist()),ctx.types())

    def visitIdlist(self,ctx:MPParser.IdlistContext)
    #idlist: ID COMMA idlist | ID;
        if(ctx.getChildCount() == 1)
            return ctx.ID().getText()
        else
            return ctx.ID().getText() & visitIdlist(self,ctx.idlist())


    def visitFuncdecl(self,ctx:MPParser.FuncdeclContext):
        local,cpstmt = self.visit(ctx.body()) 
        return FuncDecl(Id(ctx.ID().getText()),
                        [],
                        local,
                        cpstmt,
                        self.visit(ctx.mtype()))

    def visitProcdecl(self,ctx:MPParser.ProcdeclContext):
        local,cpstmt = self.visit(ctx.body()) 
        return FuncDecl(Id(ctx.ID().getText()),
                        [],
                        local,
                        cpstmt)

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
        

