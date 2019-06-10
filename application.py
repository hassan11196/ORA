from helpers2 import *

if __name__ == "__main__":
    g = Graph()
    while(True):
        print("Choose an option")
        print("1) Add Vertex")
        print("2) Add Edge")
        print("3) Display Graph")
        print("4) Display Minimum Spanning Tree")
        print("5) Simulate Minimum Spanning Tree")
        print("6) exit")

        inp = int(input("Enter Your option (1-6): "))
        
        if inp == 1:
            v = int(input("Enter Vertex Number (1-9) : "))
            if v not in g:
                g.add_vertex(v)
                print("Vertex Added.\n")
            else:
                print("Vertex Already Exists.")
        
        if inp == 2:
            src = int(input("Enter Source Vertex Number (1-9) : "))
            dest = int(input("Enter Destination Vertex Number (1-9) : "))
            weight = int(input("Enter Weight(Distance) Between Vertexes : "))
            if src not in g:
                print("Vertex " + str(src) + " not in graph")
            elif dest not in g:
                print("Vertex " + str(dest) + " not in graph")
            elif weight <= 0:
                print("Weight cannot be Zero or Negative.")
            else :
                if not g.contains_edge(src, dest):
                    g.add_edge(src, dest, weight)
                    g.add_edge(dest, src, weight)

                    print("Edge Created.")
                else:
                    print("Edge Already Exists.")
        if inp == 3:
            print("Graph.")
            g.print_graph()
            print()

        if inp == 4:
            mst = mst_prim(g)
            print("Minimum Spanning Tree.")
            mst.print_graph()
            print()

        if inp == 5:
            print("Given Graph has 7 Vertices with the following edges.")
            for i in range(0,8):
                print("added vertex " + str(i))
                g.add_vertex(i)
                
            insert_edge(g,0,3,2)
            insert_edge(g,0,2,2)
            insert_edge(g,0,7,3)
            insert_edge(g,0,1,3)
            insert_edge(g,0,6,4)
            insert_edge(g,0,5,2)
            insert_edge(g,2,4,3)
            insert_edge(g,7,4,2)
            insert_edge(g,1,4,2)
            insert_edge(g,1,6,2)

            print("Graph.")
            g.print_graph()
            print()
            mst = mst_prim(g)
            print("Minimum Spanning Tree.")
            mst.print_graph()
            print()


        if inp == 6:
            break