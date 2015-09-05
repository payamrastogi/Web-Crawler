class JupyterTest(object):
    test_var = 10
    def test(self):
        print "test"

    def test2(self):
        print self.test_var

def main():
    j = JupyterTest()
    j.test()

if __name__ == "__main__":
    main()
