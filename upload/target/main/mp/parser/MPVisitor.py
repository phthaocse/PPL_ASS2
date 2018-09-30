# Generated from main/mp/parser/MP.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MPParser import MPParser
else:
    from MPParser import MPParser

# This class defines a complete generic visitor for a parse tree produced by MPParser.

class MPVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MPParser#program.
    def visitProgram(self, ctx:MPParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#decl.
    def visitDecl(self, ctx:MPParser.DeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#var_dec.
    def visitVar_dec(self, ctx:MPParser.Var_decContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#varlist_dec.
    def visitVarlist_dec(self, ctx:MPParser.Varlist_decContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#one_var_dec.
    def visitOne_var_dec(self, ctx:MPParser.One_var_decContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#idlist.
    def visitIdlist(self, ctx:MPParser.IdlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#fun_dec.
    def visitFun_dec(self, ctx:MPParser.Fun_decContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#procedure_dec.
    def visitProcedure_dec(self, ctx:MPParser.Procedure_decContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#paralist.
    def visitParalist(self, ctx:MPParser.ParalistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#para_dec.
    def visitPara_dec(self, ctx:MPParser.Para_decContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#types.
    def visitTypes(self, ctx:MPParser.TypesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#literals.
    def visitLiterals(self, ctx:MPParser.LiteralsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#primitive_types.
    def visitPrimitive_types(self, ctx:MPParser.Primitive_typesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#compound_type.
    def visitCompound_type(self, ctx:MPParser.Compound_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#array_dec.
    def visitArray_dec(self, ctx:MPParser.Array_decContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#operand.
    def visitOperand(self, ctx:MPParser.OperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression.
    def visitExpression(self, ctx:MPParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression1.
    def visitExpression1(self, ctx:MPParser.Expression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression2.
    def visitExpression2(self, ctx:MPParser.Expression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression3.
    def visitExpression3(self, ctx:MPParser.Expression3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression4.
    def visitExpression4(self, ctx:MPParser.Expression4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression5.
    def visitExpression5(self, ctx:MPParser.Expression5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression6.
    def visitExpression6(self, ctx:MPParser.Expression6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#arrayelement.
    def visitArrayelement(self, ctx:MPParser.ArrayelementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#funcall.
    def visitFuncall(self, ctx:MPParser.FuncallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#listexp.
    def visitListexp(self, ctx:MPParser.ListexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#compoundStatement.
    def visitCompoundStatement(self, ctx:MPParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#statements.
    def visitStatements(self, ctx:MPParser.StatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#assignstatement.
    def visitAssignstatement(self, ctx:MPParser.AssignstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#variable.
    def visitVariable(self, ctx:MPParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#ifstatement.
    def visitIfstatement(self, ctx:MPParser.IfstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#whilestatement.
    def visitWhilestatement(self, ctx:MPParser.WhilestatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#forstatement.
    def visitForstatement(self, ctx:MPParser.ForstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#initialExp.
    def visitInitialExp(self, ctx:MPParser.InitialExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#finalExp.
    def visitFinalExp(self, ctx:MPParser.FinalExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#breakstatement.
    def visitBreakstatement(self, ctx:MPParser.BreakstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#continuestatement.
    def visitContinuestatement(self, ctx:MPParser.ContinuestatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#returnstatement.
    def visitReturnstatement(self, ctx:MPParser.ReturnstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#lis_statements.
    def visitLis_statements(self, ctx:MPParser.Lis_statementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#withstatements.
    def visitWithstatements(self, ctx:MPParser.WithstatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#callstatements.
    def visitCallstatements(self, ctx:MPParser.CallstatementsContext):
        return self.visitChildren(ctx)



del MPParser