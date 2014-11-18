
public class Outcast {
   private WordNet wordnet;
   // constructor takes a WordNet object
   public Outcast(WordNet wordnet) {
	   this.wordnet = wordnet;
   }

   // given an array of WordNet nouns, return an outcast
   public String outcast(String[] nouns){
	   int[] distance = new int[nouns.length];
	   
	   int i = 0;
	   for (String noun: nouns) {
		   for (String other: nouns) {
			   if (other != noun) {
				   distance[i] = distance[i] + this.wordnet.distance(noun, other);
			   }
		   }
		   i++;
	   }
	   
	   i = 0;
	   int j = 0;
	   int min = distance[j];
	   for (int d : distance) {
		   if (d < min) {
			   min = d;
			   j = i;
		   }
		   i++;
	   }
	   return nouns[j];
   }

   public static void main(String[] args) {
	    WordNet wordnet = new WordNet(args[0], args[1]);
	    Outcast outcast = new Outcast(wordnet);
	    for (int t = 2; t < args.length; t++) {
	        In in = new In(args[t]);
	        String[] nouns = in.readAllStrings();
	        StdOut.println(args[t] + ": " + outcast.outcast(nouns));
	    }
	}
}