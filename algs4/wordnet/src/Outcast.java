
public class Outcast {
	private WordNet wordnet;
	// constructor takes a WordNet object
	public Outcast(WordNet wordnet) {
		this.wordnet = wordnet;
	}

	// given an array of WordNet nouns, return an outcast
	public String outcast(String[] nouns) {
		if (nouns == null) throw new NullPointerException();

		int[] distances = new int[nouns.length];

		int i = 0;
		for (String noun: nouns) {
			for (String other: nouns) {
				if (!other.equals(noun)) {
					int distance = this.wordnet.distance(noun, other);
					distances[i] = distances[i] + distance;
					//StdOut.printf("noun: %s other: %s distance: %d acc:%d\n", noun, other, distance, distances[i]);
							
				}
			}
			i++;
		}

		i = 0;
		int j = 0;
		int max = distances[j];
		for (int d : distances) {
			if (d > max) {
				max = d;
				j = i;
			}
			i++;
		}
		return nouns[j];
	}

	public static void main(String[] args) {
		WordNet wordnet = new WordNet("synsets.txt", "hypernyms.txt");
		Outcast outcast = new Outcast(wordnet);
		String[] nouns = new String[] {"Turing", "von_Neumann", "Mickey_Mouse"};
		StdOut.printf("Exp: Mickey_Mouse Value: %s", outcast.outcast(nouns));
	}
}