// @author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
// @license This software is free - http://www.gnu.org/licenses/gpl.html

use std::collections::HashMap;

pub trait Expr {
    fn eval(&self, ctx: &HashMap<String, f64>) -> f64;
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
    fn eval(&self, ctx: &HashMap<String, f64>) -> f64 {
        let a = self.a.eval(ctx);
        let b = self.b.eval(ctx);
        match self.op.as_str() {
            "+" => a + b,
            "-" => a - b,
            "*" => a * b,
            "/" => a / b,
            _ => 0.0
        }
    }
}

pub struct Negate {
    a: Box<dyn Expr>
}
impl Negate {
    pub fn new(a: Box<dyn Expr>) -> Negate {
        Negate{ a: a }
    }
}
impl Expr for Negate {
    fn eval(&self, ctx: &HashMap<String, f64>) -> f64 {
        -self.a.eval(ctx)
    }
}

pub struct Var {
    name: String
}
impl Var {
    pub fn new(name: String) -> Var {
        Var{ name: name }
    }
}
impl Expr for Var {
    fn eval(&self, ctx: &HashMap<String, f64>) -> f64 {
        *ctx.get(&self.name).unwrap_or(&0.0)
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
    fn eval(&self, ctx: &HashMap<String, f64>) -> f64 {
        self.val
    }
}

fn from_prefix(tokens: &mut Vec<&str>) -> Box<dyn Expr> {
    let token = tokens.remove(0);
    if let Ok(v) = token.parse::<f64>() {
        Box::new(Num::new(v))
    } else {
        let a = from_prefix(tokens);
        let b = from_prefix(tokens);
        Box::new(BinaryOp::new(token.to_string(), a, b))
    } // ...
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
    println!("{}", prod2.eval(&HashMap::new()));

    let mut tokens: Vec<&str> = "* 5 + * 3 2 4".split_whitespace().collect();
    let expr = from_prefix(&mut tokens);
    println!("{}", expr.eval(&HashMap::new()));
}
