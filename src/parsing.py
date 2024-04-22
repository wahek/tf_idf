from math import log10


class Parser:
    """
    Class for counting TF | TF-IDF
    """
    def __init__(self, path, lev_dist: int = 1):
        """

        :param path: text file
        :param lev_dist: (optional attribute), maximum Levenshtein distance
        """
        self.path = path
        self.lev_dist = lev_dist
        self.text = self.parse_file()
        self.tf = self.tf_f()
        self.tf_idf = {}

        self.assumptions: set = {'а', 'е', 'ё', 'и', 'й', 'о', 'у', 'ы', 'э', 'ю', 'я'}

    def __str__(self):
        return f'({self.path=} | {self.lev_dist=})\n{self.tf=}\n{self.tf_idf=}'

    def parse_file(self) -> list[list[str]]:
        """
        Splits a text file into a list of lists [*sentence*[word, word, ...], ...]

        the function is called itself when the class is initialized and adds the self. text parameter
        """
        text = self.path.decode().lower().split('.')

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
        """
        Counts the number of occurrences of each word in the text

        the function is called itself when the class is initialized and adds the self.tf parameter
        """
        tf_count = {}

        for sentences in self.text:
            for word in sentences:
                if word in tf_count:
                    tf_count[word] += 1
                else:
                    tf_count[word] = 1

        return tf_count

    def levenshtein_distance(self, a, b) -> int:
        """
        Calculates the Levenshtein distance between two strings (words)

        (Clarification) if the last letter is a vowel and it has undergone a change, then the Levenshtein distance does
        not take it into account!!!

        :param a: first str (word)
        :param b: second str (word)
        :return: Levenshtein distance
        """
        if len(a) < len(b):
            return self.levenshtein_distance(b, a)

        if len(b) == 0:
            return len(a)

        previous_row = range(len(b) + 1)
        end = len(a) - 1
        for i, c1 in enumerate(a):
            current_row = [i + 1]
            for j, c2 in enumerate(b):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            if i == end and c1 in self.assumptions and b[-1] in self.assumptions and min(current_row) != min(previous_row):
                current_row[-1] -= 1
            previous_row = current_row
        return previous_row[-1]

    def union_tf_by_lev(self):
        """
        function combines words depending on the specified Levenshtein distance
        """
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
        """
        function for counting tf-idf
        """
        current_len = len(self.text)
        for key, value in self.tf.items():
            self.tf_idf[key] = log10(current_len / value) * value
        self.tf_idf = dict(sorted(self.tf_idf.items(), key=lambda item: item[1], reverse=True))

    def get_res_for_table(self, count: int) -> list[tuple[int, str, int, float]]:
        """
        the function aggregates data from the class (id, word, tf, tf-idf)
        :param count: number of words displayed in the table
        """
        result = []
        for i, (k, v) in enumerate(self.tf_idf.items()):
            if i == count:
                return result
            result.append((i + 1, k, self.tf[k], round(v, 3)))
        return result


if __name__ == '__main__':
    parser = Parser(b'\xef\xbb\xbf\xd0\xb9\xd1\x86\xd1\x83\xd0\xba')
    parser.union_tf_by_lev()
    parser.tf_idf_f()
    parser.get_res_for_table(10)
    print(parser)
