import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Iterator;

public class SAP {
	private Digraph G;

	// constructor takes a digraph (not necessarily a DAG)
	public SAP(Digraph G) {
		this.G = G;

	}
	
	private int calculate_ancestor(int v, int w, Integer[] v_marked, Integer[] w_marked) {
		Deque<Integer> v_queue = new ArrayDeque<Integer>();
		Deque<Integer> w_queue = new ArrayDeque<Integer>();
		
		v_queue.push(v);
		w_queue.push(w);
		int level = 0;
		v_marked[v] = level;
		w_marked[w] = level;
		
		int ancestor = -1;

		while (!v_queue.isEmpty() || !w_queue.isEmpty()) {
			level++;
			if (!v_queue.isEmpty()) {
				int v_next = v_queue.removeLast();

				if (w_marked[v_next] != null) {
					ancestor = v_next;
					break;
				}
				for (Integer i_vnext : this.G.adj(v_next)) {
					if (v_marked[i_vnext] == null) {
						v_queue.push(i_vnext);
						v_marked[i_vnext] = level;
					}
				}
			}

			if (!w_queue.isEmpty()) {
				int w_next = w_queue.removeLast();
				if (v_marked[w_next] != null) {
					ancestor = w_next;
					break;
				}

				for (Integer i_wnext : this.G.adj(w_next)) {
					if (w_marked[i_wnext] == null) {
						w_queue.push(i_wnext);
						w_marked[i_wnext] = level;
					}
				}
			}

		}
		return ancestor;
		
	}

	// length of shortest ancestral path between v and w; -1 if no such path
	public int length(int v, int w) {
		Integer[] v_marked = new Integer[this.G.V()];
		Integer[] w_marked = new Integer[this.G.V()];
		
		int ancestor = this.calculate_ancestor(v, w, v_marked, w_marked);
		return ancestor != -1 ? v_marked[ancestor] + w_marked[ancestor] : -1;
	}

	// a common ancestor of v and w that participates in a shortest ancestral
	// path; -1 if no such path
	public int ancestor(int v, int w) {
		Integer[] v_marked = new Integer[this.G.V()];
		Integer[] w_marked = new Integer[this.G.V()];
		
		int ancestor = this.calculate_ancestor(v, w, v_marked, w_marked);
		return ancestor;
	}

	// length of shortest ancestral path between any vertex in v and any vertex
	// in w; -1 if no such path
	public int length(Iterable<Integer> v, Iterable<Integer> w) {
		return -1;
	}

	// a common ancestor that participates in shortest ancestral path; -1 if no
	// such path
	public int ancestor(Iterable<Integer> v, Iterable<Integer> w) {
		return -1;
	}

	public static void main(String[] args) {
		In in = new In(args[0]);
		Digraph G = new Digraph(in);
		SAP sap = new SAP(G);

		int length = sap.length(3, 11);
		int ancestor = sap.ancestor(3, 11);
		StdOut.printf("length = %d, ancestor = %d\n", length, ancestor);
		length = sap.length(9, 12);
		ancestor = sap.ancestor(9, 12);
		StdOut.printf("length = %d, ancestor = %d\n", length, ancestor);
		length = sap.length(7, 2);
		ancestor = sap.ancestor(7, 2);
		StdOut.printf("length = %d, ancestor = %d\n", length, ancestor);
		length = sap.length(1, 6);
		ancestor = sap.ancestor(1, 6);
		StdOut.printf("length = %d, ancestor = %d\n", length, ancestor);
	}

}
