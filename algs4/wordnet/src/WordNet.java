import java.io.File;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class WordNet {

	Map<String, Integer> synsets = null;
	List<String> synsets_str = null;
	List<List<Integer>> adj = null;

	// constructor takes the name of the two input files
	public WordNet(String synsets, String hypernyms) {

		this.synsets = new HashMap<String, Integer>();
		this.adj = new ArrayList<List<Integer>>();
		this.synsets_str = new ArrayList<String>();

		In in_synsets = new In(new File(synsets));
		while (in_synsets.hasNextLine()) {
			String line = in_synsets.readLine();
			String[] items = line.split(",");
			String[] noun_synsets = items[1].split(" ");
			for (String noun: noun_synsets) {
				this.synsets.put(noun, Integer.parseInt(items[0]));
			}
			this.adj.add(new ArrayList<Integer>());
			this.synsets_str.add(items[1]);
		}
		in_synsets.close();

		In in_hypernyms = new In(new File(hypernyms));
		while (in_hypernyms.hasNextLine()) {
			String line = in_hypernyms.readLine();
			String[] items = line.split(",");
			int index = Integer.parseInt(items[0]);
			int i = 1;
			List<Integer> i_hypernyms = this.adj.get(index);
			if (i_hypernyms == null) {
				i_hypernyms = new ArrayList<Integer>();
			}
			while (i < items.length) {
				i_hypernyms.add(Integer.parseInt(items[i]));
				i++;
			}
		}
		in_hypernyms.close();
	}

	// returns all WordNet nouns
	public Iterable<String> nouns() {
		return this.synsets.keySet();
	}

	// is the word a WordNet noun?
	public boolean isNoun(String word) {
		return this.synsets.containsKey(word);
	}


	private int calculate_ancestor(String nounA, String nounB, Integer[] nounALevel,
			Integer[] nounBLevel) {
		Deque<Integer> a_queue = new ArrayDeque<Integer>();
		Deque<Integer> b_queue = new ArrayDeque<Integer>();
		Integer a_index = this.synsets.get(nounA);
		Integer b_index = this.synsets.get(nounB);

		a_queue.push(a_index);
		b_queue.push(b_index);

		int level = 0;
		int ancestor = -1;

		while (!a_queue.isEmpty() || !b_queue.isEmpty()) {
			level++;
			if (!a_queue.isEmpty()) {
				Integer aNext = a_queue.removeFirst();
				
				if (nounBLevel[aNext] != null) {
					ancestor = aNext;
					break;
				}

				for (Integer i_anext : this.adj.get(aNext)) {
					if (nounALevel[i_anext] == null) {
						a_queue.add(i_anext);
						nounALevel[i_anext] = level;
					}
				}

			}
			
			if (!b_queue.isEmpty()) {
				Integer bNext = b_queue.removeFirst();

				if (nounBLevel[bNext] != null) {
					ancestor = bNext;
					break;
				}

				for (Integer i_bnext : this.adj.get(bNext)) {
					if (nounBLevel[i_bnext] == null) {
						b_queue.add(i_bnext);
						nounBLevel[i_bnext] = level;
					}
				}	
			}

		}
		return ancestor;

	}

	// distance between nounA and nounB (defined below)
	public int distance(String nounA, String nounB){
		Integer[] nounALevel = new Integer[this.adj.size()];
		Integer[] nounBLevel = new Integer[this.adj.size()];
		int ancestor = calculate_ancestor(nounA, nounB, nounALevel, nounBLevel);
		return ancestor != -1 ? nounALevel[ancestor] + nounBLevel[ancestor] : -1;
	}

	// a synset (second field of synsets.txt) that is the common ancestor of
	// nounA and nounB
	// in a shortest ancestral path (defined below)
	public String sap(String nounA, String nounB) {
		Integer[] nounALevel = new Integer[this.adj.size()];
		Integer[] nounBLevel = new Integer[this.adj.size()];
		int ancestor = calculate_ancestor(nounA, nounB, nounALevel, nounBLevel);
		return ancestor != -1 ? this.synsets_str.get(ancestor) : null;
		
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		WordNet wordnet = new WordNet("synsets100-subgraph.txt",
				"hypernyms100-subgraph.txt");
		for (String noun : wordnet.nouns()) {
			StdOut.println(noun);

		}

		StdOut.println(String.format("Wordnet contains actin: %s",
				wordnet.isNoun("actin")));

		String nounA = "Christmas_factor";
		String nounB = "Hageman_factor";
		String expected = "coagulation_factor clotting_factor";

		StdOut.println(String.format(
				"Ancestral for {%s} and {%s} is {%s}. Expected: {%s}", nounA,
				nounB, wordnet.sap(nounA, nounB), expected));
		StdOut.println(String.format(
				"Distance for {%s} and {%s} is {%d}. Expected: {%d}", nounA,
				nounB, wordnet.distance(nounA, nounB), 2));

	}

}
