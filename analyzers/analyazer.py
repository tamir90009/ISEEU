

class Analyzer:

    def __int__(self):
        self.to_json = ''

    def analyzer(self, analyze):
        try:
            for event in analyze:
                if 'not' in event['status'].lower() or event['status'].lower() == 'ok' or 'none' in event['status'].lower() or 'checking' in event['status'].lower():
                    pass
                else:
                    print(event)

        except:
            raise Exception("Error: nothing to analyze ")