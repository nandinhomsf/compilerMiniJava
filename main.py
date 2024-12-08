from parser import parser  # Import the parser from parser.py

# Sample input data (raw source code)
data = '''
class Factorial{
    public static void main(String[] a){
        System.out.println(new Fac().ComputeFac(10));
    }
}

class Fac {
    public int ComputeFac(int num){
        int num_aux;
        if (num < 1)
            num_aux = 1;
        else
            num_aux = num * (this.ComputeFac(num-1));
        return num_aux ;
    }
}
'''

# Parse the input data directly (pass the raw string to parser)
result = parser.parse(data)  # Pass the raw source code string directly

# Print the result (AST or parse result)
print(result)
