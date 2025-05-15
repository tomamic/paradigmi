// @author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
// @license This software is free - http://www.gnu.org/licenses/gpl.html

mod syntree;
use syntree::{Expr, BinaryOp, Negate, Var, Num};
use std::collections::HashMap;

fn find_tokens(txt: &str) -> Vec<String> {
    let mut tokens : Vec<String> = Vec::new();
    let mut token = String::new();
    for c in txt.chars() {
        if c.is_ascii_alphanumeric() || c == '.' {
            token.push(c);
        } else {
            if token.len() > 0 {
                tokens.push(token.clone());
                token.clear();
            }
            if !c.is_ascii_whitespace() {
                tokens.push(c.to_string());
            }
        }
    }
    if token.len() > 0 {
        tokens.push(token.clone());
    }
    tokens
}

struct Tokenizer {
    tokens: Vec<String>,
    pos: usize
}
impl Tokenizer {
    fn new(text: &str) -> Tokenizer {
        // regex = r"\s*([A-Za-z0-9\.]+|.?)"
        Tokenizer{tokens: find_tokens(text), pos: 0}
    }

    fn peek_str(&self) -> &str {
        if let Some(x) = self.tokens.get(self.pos) {
            x.as_str()
        } else {
            ""
        }
    }

    fn peek(&self) -> String {
        String::from(self.peek_str())
    }

    fn consume(&mut self) {
        self.pos += 1;
    }

    fn consume_str(&mut self, x: &str) {
        let y = self.peek_str();
        assert!(*y == *x, "Expected {}", x);
        self.pos += 1;
    }

    fn end(&self) {
        if self.pos < self.tokens.len() {
            panic!("Extra tokens");
        }
    }
}

// expr = term {( "+" | "-" ) term}
// term = factor {( "*" | "/" ) factor}
// factor = "-" factor | "(" expr ")" | identifier | number
// (identifiers start with a letter, numbers are float)

// expr = term {( "+" | "-" ) term}
fn expr(tok: &mut Tokenizer) -> Box<dyn Expr> {
    let mut x = term(tok);
    while ["+", "-"].contains(&tok.peek_str()) {
        let op = tok.peek();
        tok.consume();
        let y = term(tok);
        x = Box::new(BinaryOp::new(op, x, y));
    }
    return x
}

// term = factor {( "*" | "/" ) factor}
fn term(tok: &mut Tokenizer) -> Box<dyn Expr> {
    let mut x = factor(tok);
    while ["*", "/"].contains(&tok.peek_str()) {
        let op = tok.peek();
        tok.consume();
        let y = factor(tok);
        x = Box::new(BinaryOp::new(op, x, y));
    }
    return x
}

// factor = "-" factor | "(" expr ")" | identifier | number
fn factor(tok: &mut Tokenizer) -> Box<dyn Expr> {
    if tok.peek_str() == "-" {
        tok.consume();
        let x = factor(tok);
        Box::new(Negate::new(x))
    } else if tok.peek_str() == "(" {
        tok.consume();
        let x = expr(tok);
        tok.consume_str(")");
        x
    } else if let Ok(v) = tok.peek_str().parse::<f64>() {
        tok.consume();
        Box::new(Num::new(v))
    } else {
        let name = tok.peek();
        tok.consume();
        Box::new(Var::new(name))
    }
}

// Tests
fn main() {
    let ctx = HashMap::from([("w".to_string(), 0.0),
                             ("x".to_string(), 1.0),
                             ("y".to_string(), 1.5),
                             ("z".to_string(), 0.5)]);

    let tests = [("(((1.5)))", "1.5", 1.5),
                 ("w * -z", "* w ~z", 0.0),
                 ("x / z * -y", "* / x z ~y", -3.0),
                 ("x / 0.5 * --y", "* / x 0.5 ~~y", 3.0),
                 ("w", "w", 0.0),
                 ("(x + w) * (x + y)", "* + x w + x y", 2.5)];

    for (infix, prefix, val) in tests {
        let mut tok = Tokenizer::new(&infix.to_string());
        let ast = expr(&mut tok);
        tok.end();
        //assert!(ast.prefix() == prefix, "Wrong prefix form");
        assert!((ast.eval(&ctx) - val).abs() < f64::EPSILON, "Wrong value");
    }
}
