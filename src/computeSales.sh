log_file="computeSales_log.txt"
paths=(
    "../data/P1/TC1.ProductList.txt"
    "../data/P2/TC1.ProductList.txt"
    "../data/P3/TC1.ProductList.txt"
)
paths2=(
    "../data/P1/TC1.TC2.Sales.txt"
    "../data/P2/TC2.TC2.Sales.txt"
    "../data/P3/TC3.TC2.Sales.txt"


)
> "$log_file"

for path in "${paths[@]}"; path2 in "${paths[@]}"; do
    echo "Testing with file: $path" | tee -a "$log_file"
    python computeSales.py -c "$path" -s "$path2" | tee -a "$log_file"
    echo "-----------------------------------" | tee -a "$log_file"
done
echo "-----------------------------------" | tee -a "$log_file"
echo "----------------PyLint-------------------" | tee -a "$log_file"
pylint computeSales.py | tee -a "$log_file"
echo "----------------flake8-------------------" | tee -a "$log_file"
flake8 computeSales.py | tee -a "$log_file"
