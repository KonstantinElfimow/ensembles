""" Вход-выход """
import ensembles


def main():
    suffix: int = 1
    # Читаем файл
    file_input = open(f'./input/input_{suffix}.txt', 'r')
    # Создаём массив непустных строк из файла
    lines = file_input.read().splitlines()
    # Закрываем файл
    file_input.close()

    # Создаём пустой словарь
    ensemble: dict = dict()

    # Добавляем ключ, значение в словарь
    for line in lines:
        line = line.split(':')
        key, value = line
        ensemble[key] = float(value)

    dependence, X, Y, X_Y, conditional_X_Y, H_x, H_y, H_x_y, Hx_y, Hy_x = ensembles.task(ensemble)
    file_output = open(f'./output/output_{suffix}.txt', 'w')
    file_output.write("Определим являются ли ансамбли X и Y независимыми\n"
                      "(независимые - заполняем '0' (без кавычек), зависимые - '1' (без кавычек)):\n" +
                      '{}'.format(dependence))
    file_output.write('\n\nВычислим X:\n')
    file_output.write('\n'.join(['p({}) = {}'.format(x, round(p, 2)) for x, p in X.items()]))
    file_output.write('\n\nВычислим Y:\n')
    file_output.write('\n'.join(['p({}) = {}'.format(y, round(p, 2)) for y, p in Y.items()]))
    file_output.write('\n\nДля определения независимости ансамблей X и Y вычислим p(x_i) * p(y_j):\n')
    file_output.write('\n'.join(['p({}) * p({}) = {}'.format(x_y.split()[0], x_y.split()[1], round(p, 2)) for x_y, p in X_Y.items()]))
    file_output.write('\n\nВычислим условные вероятности:\n')
    file_output.write('\n'.join(['p({}) = {}'.format(xy, round(p, 2)) for xy, p in conditional_X_Y.items()]))
    file_output.write('\n\nВычислим энтропию H(x):\n' + '{}'.format(round(H_x, 2)))
    file_output.write('\n\nВычислим энтропию H(y):\n' + '{}'.format(round(H_y, 2)))
    file_output.write('\n\nВычислим энтропию совместного ансамбля H(xy):\n' + '{}'.format(round(H_x_y, 2)))
    file_output.write('\n\nВычислим полную условную энтропию Hx(Y):\n' + '{}'.format(round(Hx_y, 2)))
    file_output.write('\n\nВычислим полную условную энтропию Hy(X):\n' + '{}'.format(round(Hy_x, 2)))
    file_output.close()


if __name__ == '__main__':
    main()
