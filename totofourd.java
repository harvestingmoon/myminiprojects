
import javax.swing.*; 
import java.awt.event.*;
import java.awt.*;
import java.util.ArrayList;
import java.util.Collections;


public class totofourd {
    private int count = 0;
    private int counttwo = 0;
    private JLabel label = new JLabel("Clicky test");
    private JFrame frame = new JFrame();
    JButton fourdbutton = new JButton("Press for 4D number here");
    JButton totobutton = new JButton("Press for Toto Number here");


    public totofourd() {
        
        // new Listener button thingy idkwtf it means 
        //button 1 implementation
        ActionListener test2 = new ClickListener();
        fourdbutton.addActionListener(test2);
        ActionListener listener = new ClickListener2();
        totobutton.addActionListener(listener);
        // creates new panel
        JPanel panel = new JPanel();
        panel.setBorder(BorderFactory.createEmptyBorder(30,30,10,30));
        panel.setLayout(new GridLayout(0,1));
        panel.add(fourdbutton);
        panel.add(label);
        panel.add(totobutton);
        
        // setting up frame and display 
        frame.add(panel, BorderLayout.CENTER);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setTitle("This is a random 4d toto generator");
        frame.pack();
        // ensures that the frame can be seen 
        frame.setVisible(true);

    }

    public class ClickListener implements ActionListener{
        public void actionPerformed(ActionEvent e ) {
            ArrayList<Integer> list = new ArrayList<Integer>();
            count ++;
            for (int i = 0; i < 10 ; i++) {
                list.add(i);
            }
            Collections.shuffle(list);
            StringBuilder sb = new StringBuilder();
            for ( int i = 0; i < 4; i ++) {
                int number = list.get(i);
                sb.append(number);
            }
            String result = sb.toString();
            label.setText("This is your 4d number " + result + ", you have randomed out " + count + " times ");
        }
    }

    public class ClickListener2 implements ActionListener{
        public void actionPerformed(ActionEvent e) {
            ArrayList<Integer> list = new ArrayList<Integer>();
            counttwo ++;
            for (int i = 0;i < 51; i ++) {
                list.add(i);
            }
            Collections.shuffle(list);
            StringBuilder sb = new StringBuilder();
            for (int i = 0 ; i < 7; i ++) {
                int number = list.get(i);
                sb.append(number);
                sb.append(" ");
            }
            String result = sb.toString();
            
            label.setText("This is your number \r\n " + result + " you have made " + counttwo + " different toto numbers");
        }
    }

    
    

    public static void main(String[] args) {
        new totofourd();
        
    }


    }
    
