var a int = 3

func fazalgo() int {
  var a int = 2
  Println(a)
  return a
}

func main(){
  Println(a)
  var b int = fazalgo() 
  Println(b)
}