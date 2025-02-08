import sys
import re
def main():

    result = ''
    if len(sys.argv)>1:
        input_string = sys.argv[1]

        list_algebra = ['*','-','/','//','+'] #expressões para matemática

        list_elements = list(filter(None, re.split(r'(\D)', input_string.strip())))
        list_elements = [i for i in list_elements if i != " "]
        #sprint(list_elements)
        for i in range(len(list_elements)):

            if i % 2 == 0:
                if list_elements[i] in list_algebra:
                    sys.stderr.write('conta mal estruturada')
                    return
            else:
                if list_elements[i] not in list_algebra:
                    sys.stderr.write('conta mal estruturada')
                    return

        try:
            result = eval(input_string)
            print(result)
        except Exception as e:
            sys.stderr.write(e)

    else:
        sys.stderr.write("nenhuma string foi passada")

if __name__ == '__main__':
    main()