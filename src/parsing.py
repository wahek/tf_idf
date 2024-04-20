import math


class Parser:
    def __init__(self, path, lev_dist: int = 1):
        self.path = path
        self.lev_dist = lev_dist
        self.text = self.parse_file()
        self.tf = self.tf_f()
        self.tf_idf = {}

        self.assumptions: set = {'а', 'е', 'ё', 'и', 'й', 'о', 'у', 'ы', 'э', 'ю', 'я'}

    def __str__(self):
        return f'({self.path=} | {self.lev_dist=})\n{self.tf=}\n{self.tf_idf=}'

    def parse_file(self) -> list[list[str]]:
        with open(self.path, 'r', encoding='utf-8') as f:
            """
                The function translates text from a file into a list of sentences containing a list of words.

                :param path: path to the file
            """

            text = f.read().lower().split('.')

            text = list(map(str.split, text))
            if len(text) == 1:
                text = list(text)
            for i, sentences in enumerate(text):
                for j, word in enumerate(sentences):
                    word = filter(str.isalpha, word)
                    text[i][j] = ''.join(word)
                    if text[i][j] == '':
                        text[i].pop(j)
            if not text[-1]:
                text.pop()
        return text

    def tf_f(self):
        tf_count = {}
        for sentences in self.text:
            for word in sentences:
                if word in tf_count:
                    tf_count[word] += 1
                else:
                    tf_count[word] = 1

        return tf_count

    def levenshtein_distance(self, a, b):
        if len(a) < len(b):
            return self.levenshtein_distance(b, a)

        if len(b) == 0:
            return len(a)

        previous_row = range(len(b) + 1)
        for i, c1 in enumerate(a):
            current_row = [i + 1]
            for j, c2 in enumerate(b):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            if c1 in self.assumptions and b[-1] in self.assumptions and min(current_row) != min(previous_row):
                current_row[-1] -= 1
            previous_row = current_row
        return previous_row[-1]

    def union_tf_by_lev(self):
        union_tf_count = {}
        for key, value in self.tf.items():
            if len(key) > 3:
                union_tf = {key: value}
                for k, v in self.tf.items():
                    if len(key) - len(k) in (-2, -1, 0, 1, 2) and key != k:
                        if self.levenshtein_distance(key, k) <= self.lev_dist:
                            union_tf[k] = v
                if len(union_tf) == 1:
                    union_tf_count[key] = value
                else:
                    max_tf = max(union_tf.values())
                    main = ''
                    for ku, vu in union_tf.items():
                        if vu == max_tf:
                            main = ku
                            break
                    union_tf_count[main] = sum(union_tf.values())
            else:
                union_tf_count[key] = value
        self.tf = union_tf_count

    def tf_idf_f(self):
        current_len = len(self.text)
        for key, value in self.tf.items():
            self.tf_idf[key] = math.log10(current_len / value) * value
        self.tf_idf = dict(sorted(self.tf_idf.items(), key=lambda item: item[1], reverse=True))


if __name__ == '__main__':
    parser = Parser('fake_text.txt')
    parser.union_tf_by_lev()
    parser.tf_idf_f()
    print(parser)
