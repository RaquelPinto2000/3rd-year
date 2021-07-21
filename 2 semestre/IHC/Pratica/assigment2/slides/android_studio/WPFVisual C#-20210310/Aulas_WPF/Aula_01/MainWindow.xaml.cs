using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

using System.Windows.Media.Animation;

namespace Aula_01
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void mousele_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            Console.WriteLine("Ola Mundo");
        }

      
        private void Button_MouseMove(object sender, MouseEventArgs e)
        {
            if (e.RightButton == MouseButtonState.Pressed)
                Console.WriteLine("Botão Direito");
        }

        private void mousele_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            Point p = e.GetPosition(this);
            double xPos = p.X;
            double yPos = p.Y;
            Console.WriteLine("The X Position is " + xPos + " The Y Position is " + yPos);
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            Button_1.Content = "Ola Mundo";
            //SolidColorBrush init_color = new SolidColorBrush(Colors.DarkGray);
            SolidColorBrush init_color = new SolidColorBrush(SystemColors.WindowColor);
            this.Background = init_color;
            ColorAnimation colorAnim = new ColorAnimation();
            colorAnim.Duration = new Duration(TimeSpan.FromMilliseconds(2000));
            colorAnim.To = Colors.LightGray;
            init_color.BeginAnimation(SolidColorBrush.ColorProperty,colorAnim);
        }
    }
}
