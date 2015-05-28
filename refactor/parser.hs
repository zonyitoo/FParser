module Main (main) where
import Data.Char

type Parser a = String -> [(a,String)]

result :: v -> Parser v
result v = \inp -> [(v, inp)]

zero :: Parser v
zero = \_ -> []

item :: Parser Char
item []     = []
item (x:xs) = [(x, xs)]

bind :: Parser a -> (a -> Parser b) -> Parser b
p `bind` f = \inp -> concat [f v inp' | (v,inp') <- p inp]

sat :: (Char -> Bool) -> Parser Char
sat p = item `bind` \x -> if p x then result x else zero

char :: Char -> Parser Char
char x = sat (\y -> x == y)

digit :: Parser Char
digit = sat (\x -> '0' <= x && x <= '9')

plus :: Parser a -> Parser a -> Parser a
p `plus` q = \inp -> (p inp ++ q inp)

many :: Parser a -> Parser [a]
many p = plus (bind p (\x -> bind (many p) (\xs -> result (x:xs)))) (result [])

many1 :: Parser a -> Parser [a]
many1 p = bind p (\x -> bind (many p) (\xs -> result (x:xs)))

nat :: Parser Int
nat = bind (many1 digit) (\xs -> result (eval xs))
    where
        eval xs = foldl1 op [ord x - ord '0' | x <- xs]
        m `op` n = 10 * m + n

bracket :: Parser a -> Parser b -> Parser c -> Parser b
bracket open p close = bind open (\_ -> bind p (\x -> bind close (\_ -> result x)))

chainl1 :: Parser a -> Parser (a -> a -> a) -> Parser a
p `chainl1` op = bind p (\x -> bind (inner) (\fys -> result (foldl (\x' (f,y) -> f x' y) x fys)))
    where
        inner = many (bind op (\f -> bind p (\y -> result (f,y))))

expr :: Parser Int
expr = factor `chainl1` addop

addop :: Parser (Int -> Int -> Int)
addop = plus (bind (char '+') (\_ -> result (+))) (bind (char '-') (\_ -> result (-)))

factor :: Parser Int
factor = plus nat (bracket (char '(') expr (char ')'))


main :: IO ()
main = putStrLn (show (expr "1+2"))

