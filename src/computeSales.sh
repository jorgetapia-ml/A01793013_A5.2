
log_file="computeSales_log.txt"
paths=(
    "../data/TC1/TC1.ProductList.json"
    "../data/TC2/TC1.ProductList.json"
    "../data/TC3/TC1.ProductList.json"
)
paths2=(
    "../data/TC1/TC1.Sales.json"
    "../data/TC2/TC2.Sales.json"
    "../data/TC3/TC3.Sales.json"
)

> "$log_file"

for i in "${!paths[@]}"; do
    path="${paths[$i]}"
    path2="${paths2[$i]}"
    echo "Testing with catalog file: $path and sales file: $path2" | tee -a "$log_file"
    python3 computeSales.py -c "$path" -s "$path2" | tee -a "$log_file"
    echo "-----------------------------------" | tee -a "$log_file"
done

echo "----------------PyLint-------------------" | tee -a "$log_file"
pylint computeSales.py | tee -a "$log_file"

echo "----------------flake8-------------------" | tee -a "$log_file"
flake8 computeSales.py | tee -a "$log_file"
echo "flake8 finish" | tee -a "$log_file"