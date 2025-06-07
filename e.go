func fatorial(n int) int {
  Println(n)            // ← debug: mostra cada chamada
  if (n == 1) {
    return 1
  }
  return n * fatorial(n - 1)
}

func main() {
  var resultado int = fatorial(1)
  Println(resultado)
}
