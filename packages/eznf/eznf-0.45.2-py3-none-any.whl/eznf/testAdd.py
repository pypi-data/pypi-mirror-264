import modeler

encoding = modeler.Modeler()

encoding.add_clause([2, -3])


encoding.serialize("test")
