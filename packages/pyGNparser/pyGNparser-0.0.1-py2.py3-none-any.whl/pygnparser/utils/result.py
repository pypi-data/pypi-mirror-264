class Result(dict):
    def __init__(self, parsed_result):
        super().__init__()
        self.parsed_result = parsed_result
        self.update(parsed_result)


    def _key(self, key, dict=None):
        if dict is None:
            dict = self.parsed_result
        try:
            key = dict[key]
        except KeyError:
            key = None
        return key

    
    def parsed(self):
        return self._key('parsed')


    def canonical(self):
        return self._key('canonical')

    
    def canonical_stemmed(self):
        return self._key('stemmed', dict=self.canonical())

    
    def canonical_simple(self):
        return self._key('simple', dict=self.canonical())

    
    def canonical_full(self):
        return self._key('full', dict=self.canonical())


    def authorship_details(self):
        return self._key('authorship')

    
    def authorship_verbatim(self):
        return self._key('verbatim', dict=self.authorship_details())

    
    def authorship_normalized(self):
        return self._key('normalized', dict=self.authorship_details())

    
    def authorship_year(self):
        return self._key('year', dict=self.authorship_details())

    
    def page(self):
        verbatim_authorship = self.authorship_verbatim()
        if ':' in verbatim_authorship:
            page = verbatim_authorship.split(':')[-1].strip()
        else:
            page = None
        return page

    
    def _format_authorship(self, authorship_details):
        authorship_list = authorship_details['authors']
        match len(authorship_list):
            case 0:
                authorship = ""
            case 1:
                authorship = authorship_list[0]
            case 2:
                authorship = f'{authorship_list[0]} & {authorship_list[1]}'
            case _:
                authorship = ', '.join(authorship_list[:-1]) + f' & {authorship_list[-1]}'
        if 'year' in authorship_details:
            year = self._key('year', dict=authorship_details['year'])
            authorship += f', {year}'
        if 'exAuthors' in authorship_details:
            ex_authorship = self._format_authorship(authorship_details['exAuthors'])
            authorship += f' in {ex_authorship}'
        return authorship

    
    def authorship(self):
        authorship_details = self.authorship_details()
        authorship = None
        if authorship_details is not None:
            if 'originalAuth' in authorship_details:
                authorship = self._format_authorship(authorship_details['originalAuth'])
            if 'combinationAuth' in authorship_details:
                combination_authorship = self._format_authorship(authorship_details['combinationAuth'])
                authorship = f'({authorship}) {combination_authorship}'

            # handles zoological authorship
            if 'combinationAuth' not in authorship_details and '(' in self.authorship_verbatim():
                authorship = f'({authorship})'
        return authorship


    def year(self):
        return self.authorship_year()


    def details(self):
        return self._key('details')


    def _details_rank(self):
        return list(self.details().keys())[0]


    def words(self):
        return self._key('words')


    def parser_version(self):
        return self._key('parserVersion')


    def id(self):
        return self._key('id')


    def verbatim(self):
        return self._key('verbatim')


    def normalized(self):
        return self._key('normalized')


    def quality(self):
        return self._key('quality')


    def cardinality(self):
        return self._key('cardinality')


    def tail(self):
        return self._key('tail')


    def quality_warnings(self):
        return self._key('qualityWarnings')


    def species(self):
        return self._key('species')


    def genus(self):
        return self._key('genus', dict=self.details()[self._details_rank()])


    def subgenus(self):
        return self._key('subgenus', dict=self.details()[self._details_rank()])


    def species(self):
        return self._key('species', dict=self.details()[self._details_rank()])


    def infraspecies_details(self):
        return self._key('infraspecies', dict=self.details()[self._details_rank()])


    def infraspecies(self):
        infraspecies_details = self.infraspecies_details()
        if infraspecies_details is not None:
            return self._key('value', dict=infraspecies_details[0])
        else:
            return None


    def infraspecies_rank(self):
        if self._details_rank() == 'infraspecies':
            rank = None
            if self._key('rank', dict=self.details()[self._details_rank()]['infraspecies'][0]) is not None:
                rank = self._key('rank', dict=self.details()[self._details_rank()]['infraspecies'][0])
        return rank


    def __str__(self):
            return self.parsed_result
