import java.util.ArrayDeque;
import java.util.Deque;

public class SAP {
	private Digraph G;

	// constructor takes a digraph (not necessarily a DAG)
	public SAP(Digraph G) {
		this.G = G;

	}
	
	private int calculateAncestor(Iterable<Integer> v, Iterable<Integer> w,
			Integer[] vMarked, Integer[] wMarked) {
		Deque<Integer> vQueue = new ArrayDeque<Integer>();
		Deque<Integer> wQueue = new ArrayDeque<Integer>();
		
		int level = 0;
		
		for (int item : v) {
			vQueue.push(item);
			vMarked[item] = level;
		}
		
		for (int item: w) {
			wQueue.push(item);
			wMarked[item] = level;
		}
		
		int ancestor = -1;
		int distance = Integer.MAX_VALUE;
		
		while (!vQueue.isEmpty() || !wQueue.isEmpty()) {
			if (!vQueue.isEmpty()) {
				int vNext = vQueue.removeLast();
				if (wMarked[vNext] != null) {
					if (ancestor == -1 || vMarked[vNext] + wMarked[vNext] < distance ) {
						ancestor = vNext;
						distance = vMarked[vNext] + wMarked[vNext];
					}
				}

				for (int ivNext : this.G.adj(vNext)) {
					if (vMarked[ivNext] == null) {
						vQueue.push(ivNext);
						vMarked[ivNext] = vMarked[vNext] + 1;
					}
				}
			}

			if (!wQueue.isEmpty()) {
				int wNext = wQueue.removeLast();
				if (vMarked[wNext] != null) {
					if (ancestor == -1 || vMarked[wNext] + wMarked[wNext] < distance ) {
						ancestor = wNext;
						distance = vMarked[wNext] + wMarked[wNext];
					}
				}

				for (int iwNext : this.G.adj(wNext)) {
					if (wMarked[iwNext] == null) {
						wQueue.push(iwNext);
						wMarked[iwNext] = wMarked[wNext] + 1;
					}
				}
			}

		}
		return ancestor;
		
	}

	// length of shortest ancestral path between v and w; -1 if no such path
	public int length(int v, int w) {
		Integer[] vMarked = new Integer[this.G.V()];
		Integer[] wMarked = new Integer[this.G.V()];
		
		Bag<Integer> bA = new Bag<Integer>();
		bA.add(v);
		Bag<Integer> bB = new Bag<Integer>();
		bB.add(w);
		
		int ancestor = this.calculateAncestor(bA, bB, vMarked, wMarked);
		return ancestor != -1 ? vMarked[ancestor] + wMarked[ancestor] : -1;
	}

	// a common ancestor of v and w that participates in a shortest ancestral
	// path; -1 if no such path
	public int ancestor(int v, int w) {
		Integer[] vMarked = new Integer[this.G.V()];
		Integer[] wMarked = new Integer[this.G.V()];
		
		Bag<Integer> bV = new Bag<Integer>();
		bV.add(v);
		Bag<Integer> bW = new Bag<Integer>();
		bW.add(w);
		int ancestor = this.calculateAncestor(bV, bW, vMarked, wMarked);
		return ancestor;
	}

	// length of shortest ancestral path between any vertex in v and any vertex
	// in w; -1 if no such path
	public int length(Iterable<Integer> v, Iterable<Integer> w) {
		if (v == null || w == null) throw new NullPointerException();
		Integer[] vMarked = new Integer[this.G.V()];
		Integer[] wMarked = new Integer[this.G.V()];
		int ancestor = this.calculateAncestor(v, w, vMarked, wMarked);
		if (ancestor != -1) {
			return vMarked[ancestor] + wMarked[ancestor];
		} 
		return -1;
	}

	// a common ancestor that participates in shortest ancestral path; -1 if no
	// such path
	public int ancestor(Iterable<Integer> v, Iterable<Integer> w) {
		if (v == null || w == null) throw new NullPointerException();
		Integer[] vMarked = new Integer[this.G.V()];
		Integer[] wMarked = new Integer[this.G.V()];
		return this.calculateAncestor(v, w, vMarked, wMarked);
	}

	public static void main(String[] args) {
		In in = new In("/Users/sergi/coursera/algs4/wordnet/digraph2.txt");
		Digraph G = new Digraph(in);
		SAP sap = new SAP(G);
		int length = sap.length(3, 1);
		int ancestor = sap.ancestor(3, 1);
		StdOut.printf("length = %d, ancestor = %d\n", length, ancestor);
		
		In in2 = new In("/Users/sergi/coursera/algs4/wordnet/digraph3.txt");
		G = new Digraph(in2);
		sap = new SAP(G);
		StdOut.printf("length = %d, ancestor = %d\n", sap.length(10, 7), sap.ancestor(10, 7));

		in = new In("/Users/sergi/coursera/algs4/wordnet/digraph5.txt");
		G = new Digraph(in);
		sap = new SAP(G);
		StdOut.printf("length = %d, ancestor = %d\n", sap.length(17, 21), sap.ancestor(17, 21));

		in = new In("/Users/sergi/coursera/algs4/wordnet/digraph-wordnet.txt");
		G = new Digraph(in);
		sap = new SAP(G);
		StdOut.printf("length = %d, ancestor = %d\n", sap.length(34252, 29893), sap.ancestor(34252, 29893));
		
		/*
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
		*/
		
	}

}
