op2 "+" = (+)
op2 "-" = (-)
op2 "*" = (*)
op2 "/" = (/)

data Expr = Literal Float
          | BinaryOp String Expr Expr
          deriving (Show, Read, Eq)

eval :: Expr -> Float
eval (Literal v) = v
eval (BinaryOp op a b) = (op2 op) (eval a) (eval b)

prod1 = BinaryOp "*" (Literal 3) (Literal 2)
sum1 = BinaryOp "+" prod1 (Literal 4)
prod2 = BinaryOp "*" (Literal 5) sum1

main = print $ eval prod2
