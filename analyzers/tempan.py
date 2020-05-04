import json

class Analyzer:

    def __int__(self):
        self.to_json = ''

    def analyzer(self, analyze,av):
        try:
            c=0
            f = open(r'{0}.json'.format(av), 'w')
            f.write('{')
            for event in analyze:
                c += 1
                try:
                    if 'not found' in event['status'].lower() or event['status'].lower() == 'ok' \
                            or 'none' in event['status'].lower() or 'checking' in event['status'].lower():
                        pass
                    else:
                        if len(analyze) != c:
                            print(len(analyze))
                            #f.writelines("{")
                            f.writelines(json.dumps(event)+',')
                        else:
                            f.writelines(json.dumps(event))
                except Exception as e:
                    if len(analyze) != c:
                        # f.writelines("{")
                        f.writelines(json.dumps(event) + ',')
                    else:
                        f.writelines(json.dumps(event))

            print(c)
            f.writelines("}")
            f.close()
        except:
            raise Exception("Error: nothing to analyze ")