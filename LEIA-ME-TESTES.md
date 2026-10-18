# Testes do PyComposta — migração dos testes internos

Os blocos `if __name__ == "__main__"` foram removidos dos sete módulos de geometria e suas asserções foram transferidas para `testes/test_<modulo>.py`. Cada caso é uma função `test_original_NN`. Para preservar referências entre casos, cada teste reproduz também a preparação dos casos anteriores do mesmo módulo; isso pode ser simplificado em refatoração futura.

Os testes anteriores de figuras e os seis exemplos JSON foram mantidos. O arquivo `test_modulos_originais.py`, que executava subprocessos, foi removido.

Execute na raiz do projeto:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

A pasta `geometria/` no ZIP contém a versão dos módulos utilizada para a migração. Se você fez alterações mais recentes nesses módulos, compare-as antes de substituir arquivos.

## Nomes e documentação dos testes

Os 39 testes anteriormente denominados `test_original_01`, etc., foram
renomeados para identificar as propriedades ou cenários verificados.
Cada função possui uma docstring em português. Os casos originais acumulam
verificações de etapas anteriores; a repetição foi preservada nesta revisão
para não alterar a cobertura e os resultados de referência.

Execute `python -m pytest -v` para visualizar os nomes descritivos.
