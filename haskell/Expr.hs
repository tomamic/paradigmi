module Expr where

op2 "+" = (+)
op2 "-" = (-)
op2 "*" = (*)
op2 "/" = (/)
op1 "~" = negate

data Expr = Literal Float
          | BinaryOp String Expr Expr
          deriving (Show, Read, Eq)

exprEval :: Expr -> Float
exprEval (Literal v) = v
exprEval (BinaryOp op a b) = (op2 op) (exprEval a) (eval b)

-- main = print $ eval prod2 where
--     prod1 = BinaryOp "*" (Literal 3) (Literal 2)
--     sum1 = BinaryOp "+" prod1 (Literal 4)
--     prod2 = BinaryOp "*" (Literal 5) sum1
