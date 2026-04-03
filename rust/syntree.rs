// @author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
// @license This software is free - http://www.gnu.org/licenses/gpl.html

pub trait Expr {
    fn eval(&self) -> f64;
}

pub struct BinaryOp {
    op: String,
    a: Box<dyn Expr>,
    b: Box<dyn Expr>
}
impl BinaryOp {
    pub fn new(op: String, a: Box<dyn Expr>, b: Box<dyn Expr>) -> BinaryOp {
        BinaryOp{ op: op, a: a, b: b }
    }
}
impl Expr for BinaryOp {
    fn eval(&self) -> f64 {
        let a = self.a.eval();
        let b = self.b.eval();
        match self.op.as_str() {
            "+" => a + b,
            "-" => a - b,
            "*" => a * b,
            "/" => a / b,
            _ => 0.0
        }
    }
}

pub struct Num {
    val: f64
}
impl Num {
    pub fn new(val: f64) -> Num {
        Num{ val: val }
    }
}
impl Expr for Num {
    fn eval(&self) -> f64 {
        self.val
    }
}

fn main() {
    //          *  (prod2)
    //         / \
    //        5   +  (sum1)
    //           / \
    // (prod1)  *   4
    //         / \
    //        3   2

    let prod1 = BinaryOp::new(String::from("*"), Box::new(Num::new(3.0)), Box::new(Num::new(2.0)));
    let sum1 = BinaryOp::new(String::from("+"), Box::new(Num::new(4.0)), Box::new(prod1));
    let prod2 = BinaryOp::new(String::from("*"), Box::new(sum1), Box::new(Num::new(5.0)));
    println!("{}", prod2.eval());
}
