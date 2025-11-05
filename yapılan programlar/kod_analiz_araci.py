import ast
import subprocess
import autopep8

def analyze_ast(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    variables = [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]
    print("\n--- AST Analizi ---")
    print("Fonksiyonlar:", functions)
    print("Sınıflar:", classes)
    print("Değişkenler:", set(variables))

def run_radon_analysis(file_path):
    print("\n--- Radon Analizi ---")
    try:
        subprocess.run(["radon", "cc", file_path], check=True)
        subprocess.run(["radon", "mi", file_path], check=True)
    except Exception as e:
        print("Radon analizi çalıştırılamadı:", e)

def run_flake8_analysis(file_path):
    print("\n--- Flake8 Stil Kontrolü ---")
    try:
        subprocess.run(["flake8", file_path], check=True)
    except Exception as e:
        print("Flake8 analizi çalıştırılamadı:", e)

def format_code(file_path):
    print("\n--- Autopep8 Biçimlendirme ---")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_code = f.read()
        formatted_code = autopep8.fix_code(original_code)
        new_path = file_path.replace(".py", "_formatted.py")
        with open(new_path, "w", encoding="utf-8") as f:
            f.write(formatted_code)
        print(f"Biçimlendirilmiş kod '{new_path}' dosyasına kaydedildi.")
    except Exception as e:
        print("Biçimlendirme başarısız:", e)

def main():
    file_path = input("Analiz edilecek Python dosyasının yolunu girin: ").strip()
    if not os.path.exists(file_path):
        print("Dosya bulunamadı.")
        return
    analyze_ast(file_path)
    run_radon_analysis(file_path)
    run_flake8_analysis(file_path)
    format_code(file_path)

if __name__ == "__main__":
    main()
