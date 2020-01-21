import os

import pandas as pd

# reading csv file

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 100)


class TitanicInsight:

    def __init__(self, file):
        assert isinstance(file, str) and os.path.exists(file)
        self.df = pd.read_csv(file)

    def get_survived_by_age(self, max_age):
        survived = self.df.loc[(self.df['Age'] <= max_age) & (self.df['Survived'] == 1)]
        return len(survived)

    def get_survivors_data_by_class(self):
        return self._get_max_survivors_grouped_by_col(column='Pclass')

    def _get_max_survivors_grouped_by_col(self, column):
        group_by_class = self.df.groupby([column], sort=False)
        max_survived = group_by_class['Survived'].value_counts()
        return max_survived

    def get_col_with_most_val_appearence(self):
        return self.df.count().idxmin()

    def get_survivors_data_by_title(self):
        # titles = self._titles_discovery()
        titles = {'Master\.', 'Lady\.', 'Mlle\.', 'Major\.', 'Don\.', 'Ms\.', 'Capt\.', 'Rev\.', 'Jonkheer\.', 'Mme\.',
                  'Col\.', 'Dr\.', 'Mr\.', 'Miss\.', 'Mrs\.', 'Sir\.', 'Countess\.'}

        titles = '|'.join(titles)
        s = self.df['Name'].str.extract('(' + titles + ')', expand=False)
        data_by_passangers_title = self.df.groupby(s)
        survivors_by_title = data_by_passangers_title['Survived'].value_counts()
        return survivors_by_title

    def get_survivor_count(self):
        return len(self.df.loc[self.df['Survived'] == 1])

    def count(self):
        return self.df.shape[0]

    def _titles_discovery(self):
        titles = set()
        for full_name_data in self.df['Name']:
            title = full_name_data.split(',')[1].split()[0]
            print(full_name_data)
            print(title)
            if title.endswith('.'):
                titles.add(title)
        return titles


def main():
    titanic_insight = TitanicInsight(file='./data/train.csv')
    max_age = 18
    survivors = titanic_insight.get_survived_by_age(max_age=max_age)
    print('%d passengers under %d survived' % (survivors, max_age))
    class_to_survivors_data = titanic_insight.get_survivors_data_by_class()
    class_to_survivors = dict()
    for item in class_to_survivors_data.items():
        if item[0][1] == 0:
            # not a survior
            continue
        class_to_survivors[item[0][0]] = item[1]
    best_class = max(class_to_survivors, key=class_to_survivors.get)
    print('%s is the class with most survivors: %d' % (best_class, class_to_survivors[best_class]))
    column_with_most_none_value = titanic_insight.get_col_with_most_val_appearence()
    print('%s is the col with most none values' % (column_with_most_none_value,))
    title_to_survivors_data = titanic_insight.get_survivors_data_by_title()
    desseased_count = 0
    for title_data in title_to_survivors_data.iteritems():
        survive_str = 'survived'
        if title_data[0][1] == 0:
            survive_str = 'did not survive'
            desseased_count += title_data[1]
        print('%d passengers with "%s" title %s' % (title_data[1], title_data[0][0], survive_str))
    # safety check
    real_desseased_count = titanic_insight.count() - titanic_insight.get_survivor_count()
    assert real_desseased_count == desseased_count, 'real:%d, have:%d' % (real_desseased_count, desseased_count)

    f"real:{real_desseased_count}, have:{desseased_count}"




if __name__ == "__main__":
    main()
