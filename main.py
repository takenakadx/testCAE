from lib.common import write_result,write_input,load_input,load_result
from lib.solve import solve
from lib.pre import System
from lib.post import Post

sm2 = load_input("data/input/sample.json")
output = solve(sm2)

p = Post(sm2,output)
p.show_dots_position(10.)