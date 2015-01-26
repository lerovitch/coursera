import java.io.File;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class WordNet {

	private Map<String, Integer> synsets = null;
	private List<String> synsetsStr = null;
	private List<List<Integer>> adj = null;

	// constructor takes the name of the two input files
	public WordNet(String synsets, String hypernyms) {

		this.synsets = new HashMap<String, Integer>();
		this.adj = new ArrayList<List<Integer>>();
		this.synsetsStr = new ArrayList<String>();

		In inSynsets = new In(new File(synsets));
		while (inSynsets.hasNextLine()) {
			String line = inSynsets.readLine();
			String[] items = line.split(",");
			String[] nounSynsets = items[1].split(" ");
			for (String noun: nounSynsets) {
				this.synsets.put(noun, Integer.parseInt(items[0]));
			}
			this.adj.add(new ArrayList<Integer>());
			this.synsetsStr.add(items[1]);
		}
		inSynsets.close();

		In inHypernyms = new In(new File(hypernyms));
		while (inHypernyms.hasNextLine()) {
			String line = inHypernyms.readLine();
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
		inHypernyms.close();
	}

	// returns all WordNet nouns
	public Iterable<String> nouns() {
		return this.synsets.keySet();
	}

	// is the word a WordNet noun?
	public boolean isNoun(String word) {
		if (word == null) throw new NullPointerException();
		return this.synsets.containsKey(word);
	}


	private int calculateAncestor(String nounA, String nounB, Integer[] nounALevel,
			Integer[] nounBLevel) {
		Deque<Integer> aQueue = new ArrayDeque<Integer>();
		Deque<Integer> bQueue = new ArrayDeque<Integer>();
		Integer aIndex = this.synsets.get(nounA);
		Integer bIndex = this.synsets.get(nounB);
		if (aIndex == null || bIndex == null) throw new IllegalArgumentException();

		aQueue.push(aIndex);
		nounALevel[aIndex] = 0;
		bQueue.push(bIndex);
		nounBLevel[bIndex] = 0;

		int ancestor = -1;
		int distance = Integer.MAX_VALUE;

		while (!aQueue.isEmpty() || !bQueue.isEmpty()) {
			if (!aQueue.isEmpty()) {
				Integer aNext = aQueue.removeFirst();
				
				if (nounBLevel[aNext] != null) {
					if (nounBLevel[aNext] + nounALevel[aNext] < distance) {
						ancestor = aNext;
						distance = nounBLevel[aNext] + nounALevel[aNext];
					}
				}

				for (Integer iaNext : this.adj.get(aNext)) {
					if (nounALevel[iaNext] == null) {
						aQueue.add(iaNext);
						nounALevel[iaNext] = nounALevel[aNext] + 1;
					}
				}

			}
			
			if (!bQueue.isEmpty()) {
				Integer bNext = bQueue.removeFirst();

				if (nounALevel[bNext] != null) {
					if (nounBLevel[bNext] + nounALevel[bNext] < distance) {
						ancestor = bNext;
						distance = nounBLevel[bNext] + nounALevel[bNext];
					}
				}

				for (Integer ibNext : this.adj.get(bNext)) {
					if (nounBLevel[ibNext] == null) {
						bQueue.add(ibNext);
						nounBLevel[ibNext] = nounBLevel[bNext] + 1;
					}
				}	
			}

		}
		return ancestor;

	}

	// distance between nounA and nounB (defined below)
	public int distance(String nounA, String nounB) {
		if (nounA == null || nounB == null) throw new NullPointerException();

		Integer[] nounALevel = new Integer[this.adj.size()];
		Integer[] nounBLevel = new Integer[this.adj.size()];
		int ancestor = calculateAncestor(nounA, nounB, nounALevel, nounBLevel);
		return ancestor != -1 ? nounALevel[ancestor] + nounBLevel[ancestor] : -1;
	}

	// a synset (second field of synsets.txt) that is the common ancestor of
	// nounA and nounB
	// in a shortest ancestral path (defined below)
	public String sap(String nounA, String nounB) {
		if (nounA == null || nounB == null) throw new NullPointerException();

	 	Integer[] nounALevel = new Integer[this.adj.size()];
		Integer[] nounBLevel = new Integer[this.adj.size()];
		int ancestor = calculateAncestor(nounA, nounB, nounALevel, nounBLevel);
		return ancestor != -1 ? this.synsetsStr.get(ancestor) : null;
		
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		WordNet wordnet = new WordNet("synsets100-subgraph.txt",
				"hypernyms100-subgraph.txt");

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

		wordnet = new WordNet("synsets.txt", "hypernyms.txt");
		StdOut.printf("Distance: %d Expected: 12\n", wordnet.distance("genus_Melanerpes", "inti"));
		StdOut.printf("Sap: %s Expected: 'abstraction abstract_entity'\n", wordnet.sap("genus_Melanerpes", "inti"));

		wordnet = new WordNet("synsets11.txt", "hypernyms11AmbiguousAncestor.txt");
		StdOut.printf("Distance: %d\n", wordnet.distance("a", "b"));
		
		wordnet = new WordNet("synsets500-subgraph.txt", "hypernyms500-subgraph.txt");
		StdOut.printf("Distance: %d Expected: 7\n", wordnet.distance("tetrose", "invertase"));
		StdOut.printf("Sap: '%s' Expected: 'macromolecule supermolecule'\n", wordnet.sap("tetrose", "invertase"));
	}

}
