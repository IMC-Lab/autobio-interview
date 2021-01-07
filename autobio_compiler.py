import csv, pandas as pd
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc

class MatchRetokenizeComponent:
  def __init__(self, nlp, terms):
    self.terms = terms
    self.matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(text) for text in terms]
    self.matcher.add("TerminologyList", None, *patterns)
    Doc.set_extension("phrase_matches", getter=self.matcher, force=True)

  def __call__(self, doc):
    matches = self.matcher(doc)
    with doc.retokenize() as retokenizer:
        for match_id, start, end in matches:
            retokenizer.merge(doc[start:end], attrs={"LEMMA": str(doc[start:end])})
    return doc

terms = ["[ed-int]",
         "[ed-ext]",
         "[pl-int]",
         "[pl-ext]",
         "[t-int]",
         "[t-ext]",
         "[perc-int]",
         "[perc-ext]",
         "[tho-int]",
         "[tho-ext]",
         "[emo-int]",
         "[emo-ext]",
         "[sem-per]",
         "[sem-gen]",
         "[other]",
         "[rep]"]
nlp = English()
retokenizer = MatchRetokenizeComponent(nlp, terms)
nlp.add_pipe(retokenizer, name='merge_phrases', last=True)

def phenregcompile(fname, output):
    with open(fname, 'r+', encoding="utf-8-sig", newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        next(filereader)
        counter = 0
        finalData = {}
        for row in filereader:
            segments = []
            words = nlp(row[4])
            tokens = [token.text for token in words]
            segments.append(tokens.count('[ed-int]'))
            segments.append(tokens.count('[pl-int]'))
            segments.append(tokens.count('[t-int]'))
            segments.append(tokens.count('[perc-int]'))
            segments.append(tokens.count('[tho-int]'))
            segments.append(tokens.count('[ed-ext]'))
            segments.append(tokens.count('[pl-ext]'))
            segments.append(tokens.count('[t-ext]'))
            segments.append(tokens.count('[perc-ext]'))
            segments.append(tokens.count('[tho-ext]'))
            segments.append(tokens.count('[sem-per]'))
            segments.append(tokens.count('[sem-gen]'))
            segments.append(tokens.count('[rep]'))
            segments.append(tokens.count('[other]'))
            segments.append(sum(segments))
            finalData['trial'+str(counter)] = segments
            counter += 1
    df1 = pd.DataFrame.from_dict(finalData)
    df1_transposed = df1.T
    df1_transposed.to_csv(output, index = False)


if __name__ == '__main__':
    phenregcompile('PhenReg_NL.csv',r'FullTestNL.csv')
    phenregcompile('PhenReg_SH.csv',r'FullTestSH.csv')